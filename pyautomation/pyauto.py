"""
pyautomation for Python 3.
Author: iamtony.ca@gmail.com
Source: https://github.com/changgwak/python-automation

This module is for Automation on Windows os.
With the pyautomation package, you can control your GUI automatically while simultaneously controlling the mouse and keyboard physically, similar to how selenium automates web browsers.
Read 'readme.md' for help.

pyautomation is shared under the MIT Licene.
This means that the code can be freely copied and distributed, and costs nothing to use.
"""

from . import msuiauto as msauto
# import msuiauto as msauto

import logging
import os
import json
from typing import Callable, List, Optional, Tuple, Any, Type
import win32gui
import win32con
import win32api
from functools import wraps
import time
import asyncio
from pydantic import BaseModel, ValidationError
from injector import Injector, inject, singleton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from enum import Enum, auto

# Load environment variables from .env file
load_dotenv()

# Setup structured logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Control profiling log output
PROFILE_LOGGING_ENABLED = os.getenv('PROFILE_LOGGING_ENABLED', 'False').lower() == 'true'

# Control comtypes DEBUG logs
COMTYPES_DEBUG_LOGGING_ENABLED = os.getenv('COMTYPES_DEBUG_LOGGING_ENABLED', 'False').lower() == 'true'
comtypes_logger = logging.getLogger('comtypes')
comtypes_logger.setLevel(logging.DEBUG if COMTYPES_DEBUG_LOGGING_ENABLED else logging.WARNING)

class WinAutoError(Exception):
    """Custom exception for WinAuto errors."""
    pass

class LogLevel(Enum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()

def log_exceptions(level: LogLevel = LogLevel.ERROR):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.log(level.value, f"Exception in {func.__name__}: {e}")
                raise
        return wrapper
    return decorator

def profile(func):
    """A decorator that profiles the execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # PROFILE_LOGGING_ENABLED = False
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        if PROFILE_LOGGING_ENABLED:
            logging.info(f"Function {func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

class Config(BaseModel):
    desired_parent_name: Optional[str] = ""
    desired_child_name: Optional[str] = ""
    # scale_factor: Optional[float] = None
    monitor_index: Optional[int] = None

class ConfigLoader:
    """A class responsible for loading configuration."""
    
    @staticmethod
    def load_config(file_path=None, **kwargs) -> Config:
        # with open(file_path, 'r') as config_file:
        #     config_data = json.load(config_file)

        # Default parameters
        config_data = {
                "desired_parent_name": "app_usage.py - python-autoevent - Visual Studio Code",
                "desired_child_name": "GitLens Inspect",
                # "scale_factor": 1.5,
                "monitor_index": 1
            }
        # print(type(data))
        if file_path is not None:
            # Check if input is a file path
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    file_data = json.load(file)
                    config_data.update(file_data)
            else:
                try:
                    json_data = json.loads(file_path)
                    config_data.update(json_data)
                except json.JSONDecodeError:
                    print("Invalid JSON data")
                    return None
        else:
            config_data.update(kwargs)


        # print("********************", config_data)
        return Config(**config_data)




@singleton
class WinAuto:
    @inject
    def __init__(self, config: Config = None):
        self.config = config
        self.scale_factor = self.get_scale_factor()

    def get_scale_factor(self):
    #     import displayinfo as pydis
    #     scale_factors=pydis.DisplayInfo().get_scale_factor(pydis.DisplayInfo().get_Qapp())
    #     return scale_factors[self.config.monitor_index-1]
        return None

    @log_exceptions(LogLevel.ERROR)
    def get_info(self, control: Any, depth: int = 0, delimiter: str = "") -> None:
        """Prints information about the control."""
        child_handle = control.NativeWindowHandle
        child_name = control.Name
        child_controltype = control.LocalizedControlType
        child_location = control.BoundingRectangle
        child_classname = control.ClassName
        logger.info(f"{delimiter} Depth: {depth}, Window Handle: {child_handle}, name: {child_name}, control_type: {child_controltype}, location: {child_location}, classname: {child_classname}")

    @log_exceptions(LogLevel.ERROR)
    def get_relative_location(self, parent_control: Any, child_control: Any) -> Tuple[int, int]:
        """Calculates the relative location of the child control to the parent control."""
        parent_rectangle = parent_control.BoundingRectangle
        child_rectangle = child_control.BoundingRectangle

        relative_x = child_rectangle.left - parent_rectangle.left
        relative_y = child_rectangle.top - parent_rectangle.top

        center_x = child_rectangle.left + (child_rectangle.width() // 2)
        center_y = child_rectangle.top + (child_rectangle.height() // 2)

        relative_center_x = center_x - parent_rectangle.left
        relative_center_y = center_y - parent_rectangle.top

        return relative_center_x, relative_center_y

    @profile
    @log_exceptions(LogLevel.ERROR)
    def walk_and_find(self, control: Any, depth: int = 0, debug: bool = False) -> Tuple[Optional[Any], Optional[int]]:
        """Recursively finds a control by name."""
        condition = lambda c: c.Name == self.config.desired_child_name
        if condition(control):
            return control, depth
        for child in control.GetChildren():
            if debug is False: pass
            elif debug is True: self.get_info(child, depth, "**child")
            result, result_depth = self.walk_and_find(child, depth + 1)
            if result:
                return result, result_depth
        return None, None

    @profile
    @log_exceptions(LogLevel.ERROR)
    def walk_and_find_all(self, control: Any, condition: Optional[Callable[[Any], bool]] = None, depth: int = 0) -> List[Tuple[Any, int]]:
        """Recursively finds all controls that match the condition."""
        found_controls = []
        if condition is None:
            condition = lambda x: True

        if condition(control):
            found_controls.append((control, depth))

        for child in control.GetChildren():
            self.get_info(child, depth, "****child")
            found_controls.extend(self.walk_and_find_all(child, condition, depth + 1))

        return found_controls

    @log_exceptions(LogLevel.ERROR)
    def click_relative_location(self, parent_control: Any, x: int, y: int) -> None:
        """Clicks at a relative location within the parent control."""
        hWnd = parent_control.NativeWindowHandle
        lParam = win32api.MAKELONG(x, y)
        win32gui.PostMessage(hWnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        win32gui.PostMessage(hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32api.Sleep(100)
        win32gui.PostMessage(hWnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)

    @log_exceptions(LogLevel.ERROR)
    def click_enter_relative_location(self, parent_control: Any, x: int, y: int) -> None:
        """Clicks at a relative location and presses enter."""
        self.click_relative_location(parent_control, x, y)
        hWnd = parent_control.NativeWindowHandle
        win32gui.PostMessage(hWnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.PostMessage(hWnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

    @log_exceptions(LogLevel.ERROR)
    def click_direct_child(self, child_control: Any) -> None:
        """Clicks directly on a child control."""
        hwnd = child_control.NativeWindowHandle
        win32gui.PostMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
        win32api.Sleep(100)
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)

    @log_exceptions(LogLevel.ERROR)
    def type_text(self, hwnd: int, text: str) -> None:
        """Types text into a window."""
        for char in text:
            if char == "\n":
                win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
            else:
                win32gui.PostMessage(hwnd, win32con.WM_CHAR, ord(char), 0)

    @log_exceptions(LogLevel.ERROR)
    def hotkey_event(self) -> None:
        """Placeholder for handling hotkey events."""
        pass

    @log_exceptions(LogLevel.ERROR)
    def get_all_children(self, root: Any) -> None:
        """Gets and logs information about all child controls."""
        children = root.GetChildren()
        for child in children:
            self.get_info(child, 0, "GetChildren")

    @log_exceptions(LogLevel.ERROR)
    def click_at(self, x: int, y: int, visible: bool = False, scale_factor: Optional[float] = None) -> None:
        """Clicks at a specified screen location, optionally scaled and made visible."""
        try:
            if scale_factor is not None :
                scale_factor_monitor = scale_factor
            elif scale_factor is None:
                scale_factor_monitor = self.scale_factor

            # print("scale_factor_monitor: ", scale_factor_monitor)
            scaled_x, scaled_y = self._apply_scaling(x, y, scale_factor_monitor)
            if visible:
                self._visible_click(scaled_x, scaled_y)
            else:
                self._invisible_click(scaled_x, scaled_y)
        except Exception as e:
            logger.error(f"Error in click_at: {e}")
            raise WinAutoError("Failed to click at specified location")


    def _apply_scaling(self, x: int, y: int, scale_factor: Optional[float]) -> Tuple[int, int]:
        scale_factor = 1.0
        if scale_factor:
            return round(x / scale_factor), round(y / scale_factor)
        return x, y

    def _visible_click(self, x: int, y: int) -> None:
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def _invisible_click(self, x: int, y: int) -> None:
        hwnd = win32gui.WindowFromPoint((x, y))
        if hwnd:
            client_coords = win32gui.ScreenToClient(hwnd, (x, y))
            lParam = win32api.MAKELONG(client_coords[0], client_coords[1])
            win32gui.PostMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
            win32api.Sleep(100)
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)




    @log_exceptions(LogLevel.ERROR)
    async def async_click_at(self, x: int, y: int, visible: bool = False, scale_factor: Optional[float] = None) -> None:
        """Asynchronously clicks at a specified screen location, optionally scaled and made visible."""
        try:
            if scale_factor is not None :
                scale_factor_monitor = scale_factor
            elif scale_factor is None:
                scale_factor_monitor = self.scale_factor
            
            scaled_x, scaled_y = self._apply_scaling(x, y, scale_factor_monitor)
            if visible:
                await self._async_visible_click(scaled_x, scaled_y)
            else:
                await self._async_invisible_click(scaled_x, scaled_y)
        except Exception as e:
            logger.error(f"Error in async_click_at: {e}")
            raise WinAutoError("Failed to asynchronously click at specified location")

    async def _async_visible_click(self, x: int, y: int) -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._visible_click, x, y)

    async def _async_invisible_click(self, x: int, y: int) -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._invisible_click, x, y)

    @log_exceptions(LogLevel.ERROR)
    def load_plugin(self, plugin_name: str) -> None:
        """Dynamically loads a plugin for additional UI interactions."""
        try:
            module = __import__(plugin_name)
            plugin_class = getattr(module, 'Plugin')
            plugin_instance = plugin_class(self)
            plugin_instance.register()
            logger.info(f"Plugin {plugin_name} loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_name}: {e}")

    @log_exceptions(LogLevel.ERROR)
    def schedule_task(self, func: Callable, cron_expression: str) -> None:
        """Schedules a task using a cron expression."""
        scheduler = AsyncIOScheduler()
        trigger = CronTrigger.from_crontab(cron_expression)
        scheduler.add_job(func, trigger)
        scheduler.start()
        logger.info(f"Task {func.__name__} scheduled with cron expression {cron_expression}")

    @log_exceptions(LogLevel.ERROR)
    def transform_scale(self, scale_factor: float) -> None:
        """Transforms the scale factor used for UI operations."""
        self.scale_factor = scale_factor

# Example usage
if __name__ == "__main__":
    try:
        # Load configuration
        config_path = os.getenv('WIN_AUTO_CONFIG', 'config.json')
        config = ConfigLoader.load_config(config_path)

        # Set up dependency injection
        injector = Injector()
        injector.binder.bind(Config, to=config)

        # Initialize WinAuto with configuration
        ap = injector.get(WinAuto)
        
        # Example synchronous click
        ap.click_at(38, 864, visible=False, scale_factor=1.75)
        
        time.sleep(1.5)
        # Example asynchronous click
        asyncio.run(ap.async_click_at(38, 864, visible=False, scale_factor=1.75))
        
        # Load a plugin
        ap.load_plugin('example_plugin')
        
        # Schedule a task
        ap.schedule_task(lambda: ap.click_at(150, 30), '*/5 * * * *')

    except WinAutoError as e:
        logger.error(f"An error occurred: {e}")
    except ValidationError as e:
        logger.error(f"Configuration validation error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

# Unit Tests using pytest
def test_get_relative_location():
    class MockControl:
        def __init__(self, left, top, right, bottom):
            self.BoundingRectangle = self.Rectangle(left, top, right, bottom)

        class Rectangle:
            def __init__(self, left, top, right, bottom):
                self.left = left
                self.top = top
                self.right = right
                self.bottom = bottom

    parent_control = MockControl(10, 10, 50, 50)
    child_control = MockControl(20, 20, 40, 40)
    
    wa = WinAuto(config=Config())
    relative_x, relative_y = wa.get_relative_location(parent_control, child_control)
    assert relative_x == 15  # Center x-coordinate of child relative to parent
    assert relative_y == 15  # Center y-coordinate of child relative to parent

def test_click_relative_location(mocker):
    # Mock win32api and win32gui functions
    mock_post_message = mocker.patch('win32gui.PostMessage')
    mock_sleep = mocker.patch('win32api.Sleep')
    mock_make_long = mocker.patch('win32api.MAKELONG', return_value=100)

    class MockControl:
        NativeWindowHandle = 12345

    parent_control = MockControl()
    wa = WinAuto(config=Config())
    wa.click_relative_location(parent_control, 10, 10)

    mock_post_message.assert_any_call(parent_control.NativeWindowHandle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    mock_post_message.assert_any_call(parent_control.NativeWindowHandle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 100)
    mock_sleep.assert_called_once_with(100)
    mock_post_message.assert_any_call(parent_control.NativeWindowHandle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 100)

def test_click_at_visible(mocker):
    # Mock win32api functions
    mock_set_cursor_pos = mocker.patch('win32api.SetCursorPos')
    mock_mouse_event = mocker.patch('win32api.mouse_event')

    wa = WinAuto(config=Config())
    wa.click_at(150, 30, visible=True)

    mock_set_cursor_pos.assert_called_once_with((150, 30))
    mock_mouse_event.assert_any_call(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    mock_mouse_event.assert_any_call(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def test_click_at_invisible(mocker):
    # Mock win32api and win32gui functions
    mock_window_from_point = mocker.patch('win32gui.WindowFromPoint', return_value=12345)
    mock_screen_to_client = mocker.patch('win32gui.ScreenToClient', return_value=(10, 10))
    mock_post_message = mocker.patch('win32gui.PostMessage')
    mock_make_long = mocker.patch('win32api.MAKELONG', return_value=100)
    mock_sleep = mocker.patch('win32api.Sleep')

    wa = WinAuto(config=Config())
    wa.click_at(150, 30, visible=False)

    mock_window_from_point.assert_called_once_with((150, 30))
    mock_screen_to_client.assert_called_once_with(12345, (150, 30))
    mock_post_message.assert_any_call(12345, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    mock_post_message.assert_any_call(12345, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 100)
    mock_sleep.assert_called_once_with(100)
    mock_post_message.assert_any_call(12345, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 100)

# More tests can be added for each method to ensure all edge cases are covered.
