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

from PyQt5.QtWidgets import QApplication
from .modules.screeninfo.screeninfo import get_monitors
from .modules import mss
import sys

class DisplayInfo():
    def __init__(self):
        self.scale_factor = []
        self.display_info = []
        self.display_info_ = []
        self.is_app_generated = False
        self.app = None

    def get_Qapp(self):
        if self.is_app_generated == False:
            self.app = QApplication(sys.argv)
            self.is_app_generated = True
        return self.app

    def get_scale_factor(self, app):
        screens = app.screens()
        monitor_order = get_monitors()  # Get the monitors in Windows display order
        # print(f"monitor_order: {monitor_order}")
        # screen_dict = {screen.geometry().topLeft(): screen for screen in screens}
        # screen_dict = {tuple(screen.geometry().topLeft()): screen for screen in screens}
        screen_dict = {(screen.geometry().topLeft().x(), screen.geometry().topLeft().y()): screen for screen in screens}
        # print(f"screen_dict: {screen_dict}")


        for monitor in monitor_order:
            pos = (monitor.x, monitor.y)
            # print(f"pos: {pos}")
            screen = screen_dict.get(pos)
            # print(f"screen: {screen}")
            if screen:
                logical_dpi = screen.logicalDotsPerInch()
                self.scale_factor.append(logical_dpi / 96.0)  # Based on Windows' standard DPI of 96
        return self.scale_factor

    def get_screen_info_(self):
        app = self.get_Qapp()
        screens = app.screens()
        for i, screen in enumerate(screens):
            self.display_info_.append(f"Screen {i+1}: {screen.geometry()}")
        return self.display_info_

    def get_screen_info(self):
        for m in get_monitors():
            self.display_info.append(str(m))
        return self.display_info

    def capture_screen(self) -> any:
            with mss.mss() as sct:
                monitor = sct.monitors
            return monitor



if __name__ == "__main__":
    dis = DisplayInfo()
    app = dis.get_Qapp()
    print(dis.get_scale_factor(app))
    print("##############")
    print(dis.get_screen_info_())
    print("##############")
    print(dis.get_screen_info())
    print("##############")
    print(dis.capture_screen())


