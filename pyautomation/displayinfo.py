# from .modules.PyQt5.QtWidgets import QApplication
from .modules.screeninfo.screeninfo import get_monitors
from .modules.mss import mss
from PyQt5.QtWidgets import QApplication

import sys

class DisplayInfo():
    def __init__(self):
        self.app = QApplication(sys.argv)
        # self.screens = app.screens()
        self.scale_factor = []
        self.display_info = []
        pass
        

    def get_scale_factor(self):
        screens = self.app.screens()
        for i, screen in enumerate(screens):
            logical_dpi = screen.logicalDotsPerInch()
            self.scale_factor.append(logical_dpi / 96.0)  # Based on Windows' standard DPI of 96
            # print(f"Monitor {i+1}: Scale Factor = {self.scale_factor}")
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
#     print(dis.get_screen_info())
#     print(dis.get_scale_factor())
    