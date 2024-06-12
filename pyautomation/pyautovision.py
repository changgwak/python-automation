
import cv2
import numpy as np
from .modules import mss
import logging
import asyncio
from typing import Optional, Tuple, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
import aiofiles
import yaml
import argparse
import os
from pydantic import BaseModel, ValidationError, validator
from injector import Injector, inject, Module, singleton, provider
from dataclasses import dataclass, field

# Structured logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ConfigModel(BaseModel):
    monitor_index: int
    ratio: float
    min_match_count: int

    @validator('ratio')
    def ratio_must_be_between_0_and_1(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('ratio must be between 0 and 1')
        return v

class ConfigModule(Module):
    def __init__(self, config_path: str):
        self.config_path = config_path

    @singleton
    @provider
    def provide_config(self) -> ConfigModel:
        with open(self.config_path, 'r') as file:
            config_dict = yaml.safe_load(file)
        try:
            return ConfigModel(**config_dict)
        except ValidationError as e:
            logging.error(f"Configuration validation error: {e}")
            raise

@dataclass
class ImageMatcher:
    template_path: str
    config: ConfigModel

    template_image: Optional[np.ndarray] = field(init=False, default=None)
    screenshot_image: Optional[np.ndarray] = field(init=False, default=None)
    matches: Optional[List] = field(init=False, default=None)
    good_matches: Optional[List] = field(init=False, default=None)
    object_location: Optional[np.ndarray] = field(init=False, default=None)
    object_center: Optional[Tuple[int, int]] = field(init=False, default=None)

    @inject
    def __post_init__(self):
        pass

    async def load_image(self, path: str, grayscale: bool = True) -> np.ndarray:
        async with aiofiles.open(path, mode='rb') as f:
            image_data = await f.read()
        image_array = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR)
        if image is None:
            logging.error(f"Image not found at path: {path}")
            raise FileNotFoundError(f"Image not found at path: {path}")
        logging.info(f"Image loaded from path: {path}")
        return image

    async def capture_screen(self) -> None:
        with mss.mss() as sct:
            monitor = sct.monitors[self.config.monitor_index]  # Configurable monitor index
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            self.screenshot_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            logging.info("Screen captured successfully")

    @staticmethod
    async def find_features(image: np.ndarray) -> Tuple[List[cv2.KeyPoint], np.ndarray]:
        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(image, None)
        return keypoints, descriptors

    @staticmethod
    def match_features(des1: np.ndarray, des2: np.ndarray) -> List:
        index_params = dict(algorithm=1, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)
        return matches

    @staticmethod
    def filter_good_matches(matches: List, ratio: float) -> List:
        return [m for m, n in matches if m.distance < ratio * n.distance]

    def find_object_location(
        self, kp1: List[cv2.KeyPoint], kp2: List[cv2.KeyPoint], good_matches: List, min_match_count: int
    ) -> Tuple[Optional[Tuple[int, int]], Optional[np.ndarray]]:
        if len(good_matches) > min_match_count:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            h, w = self.template_image.shape[:2]
            pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            self.object_location = np.int32(dst)
            self.object_center = (int((dst[0][0][0] + dst[2][0][0]) / 2), int((dst[0][0][1] + dst[2][0][1]) / 2))
        else:
            logging.warning(f"Not enough matches are found - {len(good_matches)}/{min_match_count}")
            self.object_location = None
            self.object_center = None
        
        return self.object_center, self.object_location

    def draw_object_location(self, color: Tuple[int, int, int] = (0, 255, 0), thickness: int = 3) -> None:
        if self.object_location is not None:
            input_image_bgr = cv2.cvtColor(self.screenshot_image, cv2.COLOR_GRAY2BGR)
            input_image_bgr = cv2.polylines(input_image_bgr, [self.object_location], True, color, thickness, cv2.LINE_AA)
            cv2.imshow("Template Image", self.template_image)
            cv2.imshow("Detected Object", input_image_bgr)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            logging.info("No object location found to draw")

    async def process_image(self) -> None:
        kp1, des1 = await self.find_features(self.template_image)
        kp2, des2 = await self.find_features(self.screenshot_image)
        matches = self.match_features(des1, des2)
        good_matches = self.filter_good_matches(matches, self.config.ratio)
        self.find_object_location(kp1, kp2, good_matches, self.config.min_match_count)
        logging.info("Image processing completed")

    async def run(self) -> None:
        self.template_image = await self.load_image(self.template_path)
        await self.capture_screen()
        await self.process_image()
        logging.info(f"Object center: {self.object_center}")
        self.draw_object_location()

    async def get_object_location(self) -> Tuple[Optional[Tuple[int, int]], Optional[np.ndarray]]:
        await self.run()
        return self.object_center, self.object_location

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Image Matcher Configuration")
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to the configuration file')
    parser.add_argument('--template', type=str, required=True, help='Path to the template image')
    return parser.parse_args()

def main():
    args = parse_args()
    injector = Injector([ConfigModule(args.config)])
    matcher = injector.create_object(ImageMatcher, additional_kwargs={'template_path': args.template})
    asyncio.run(matcher.run())

if __name__ == "__main__":
    main()

## Example of config.yaml
# monitor_index: 1
# ratio: 0.7
# min_match_count: 10


## Usage(sh)
# python your_script.py --template path_to_your_template_image.jpg --config path_to_your_config.yaml
