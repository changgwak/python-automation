from .modules.screeninfo.screeninfo import get_monitors
##

class DisplayInfo():
    def __init__(self):
        pass
    def get_screen_info(self):
        for m in get_monitors():
            print(str(m))


# test = DisplayInfo()
# test.get_screen_info()