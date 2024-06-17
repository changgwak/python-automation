import os
# import json
# import asyncio
from ..pyauto import ConfigLoader, WinAuto
# from injector import Injector

def load_test_config():
    # Ensure the config.json file is in the same directory as test.py
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    return ConfigLoader.load_config(config_path)

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
    
    config = load_test_config()
    wa = WinAuto(config=config)
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
    config = load_test_config()
    wa = WinAuto(config=config)
    wa.click_relative_location(parent_control, 10, 10)

    mock_post_message.assert_any_call(parent_control.NativeWindowHandle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    mock_post_message.assert_any_call(parent_control.NativeWindowHandle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 100)
    mock_sleep.assert_called_once_with(100)
    mock_post_message.assert_any_call(parent_control.NativeWindowHandle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 100)

def test_click_at_visible(mocker):
    # Mock win32api functions
    mock_set_cursor_pos = mocker.patch('win32api.SetCursorPos')
    mock_mouse_event = mocker.patch('win32api.mouse_event')

    config = load_test_config()
    wa = WinAuto(config=config)
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

    config = load_test_config()
    wa = WinAuto(config=config)
    wa.click_at(150, 30, visible=False)

    mock_window_from_point.assert_called_once_with((150, 30))
    mock_screen_to_client.assert_called_once_with(12345, (150, 30))
    mock_post_message.assert_any_call(12345, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    mock_post_message.assert_any_call(12345, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 100)
    mock_sleep.assert_called_once_with(100)
    mock_post_message.assert_any_call(12345, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 100)

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
