from modules import mss
import cv2
import numpy as np


def capture_screen() -> None:
    with mss.mss() as sct:
        print(sct)
        monitor = sct.monitors[0]  # Configurable monitor index
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        screenshot_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print("print(img.shape) : ", print(img.shape))
        cv2.imshow("Detected Object", screenshot_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


capture_screen()