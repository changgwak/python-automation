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


# from .modules.PyQt5.QtWidgets import QApplication
from .modules.screeninfo.screeninfo import get_monitors
from .modules import mss
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

import sys

class DisplayInfo():
    def __init__(self):
   
        self.scale_factor = []
        self.display_info = []
        self.is_app_generated =False
        self.app = None
        # self.get_scale_factor()
        pass

    def get_Qapp(self):
        if self.is_app_generated == False :
            self.app = QApplication(sys.argv)
            self.is_app_generated = True
        return self.app

    def get_scale_factor(self, app):
        screens = app.screens()
        for i, screen in enumerate(screens):
            logical_dpi = screen.logicalDotsPerInch()
            # print(screen, logical_dpi)
            self.scale_factor.append(logical_dpi / 96.0)  # Based on Windows' standard DPI of 96
        #     # print(f"Monitor {i+1}: Scale Factor = {self.scale_factors}")
        return self.scale_factor
    

    def get_screen_info(self):
        for m in get_monitors():
            self.display_info.append(str(m))
            # print(str(m))
        return self.display_info

    def print_scale_factors(self):
        screens = self.app.screens()
        for i, screen in enumerate(screens):
            logical_dpi = screen.logicalDotsPerInch()
            self.scale_factor = logical_dpi / 96.0  # Based on Windows' standard DPI of 96
            print(f"Monitor {i+1}: Scale Factor = {self.scale_factor}")

    def print_screen_info(self):
        for m in get_monitors():
            # self.display_info = self.display_info.append(str(m))
            print(str(m))

    def sreenshot(self):
        # The simplest use, save a screen shot of the 1st monitor
        with mss() as sct:
            sct.shot()



# if __name__ == "__main__":
#     dis = DisplayInfo()
#     # dis.print_scale_factors()
#     # dis.print_screen_info()
#     # print(dis.get_screen_info())
#     print(dis.get_scale_factor(dis.get_Qapp()))
    
