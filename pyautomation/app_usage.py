## Handle Usage
import os, time
import pyautomation.pyauto as pyapp
os.system ('notepad.exe')
time.sleep(3)
window = pyapp.msauto.WindowControl(searchDepth=1, ClassName='Notepad')

config = pyapp.ConfigLoader.load_config(desired_parent_name= window.Name, desired_child_name= "Text editor")
wa = pyapp.WinAuto(config=config)
result, depth = wa.walk_and_find(window)
wa.type_text(result.NativeWindowHandle, "hello notepad!")



## Load configuration
# config_path = r'.\config\pyauto.json'
# config = pyauto.ConfigLoader.load_config(config_path)
config = pyapp.ConfigLoader.load_config(desired_parent_name= "test.py - python-autoevent - Visual Studio Code", desired_child_name= "Docker", monitor_index=1)

wa = pyapp.WinAuto(config=config)


## search parent and child
root = pyapp.msauto.PaneControl(Name=config.desired_parent_name)

child, child_depth = wa.walk_and_find(root, debug=True)
wa.get_info(child, child_depth, "Target")
wa.get_info(child.GetParentControl(), child_depth-1, "Target Parent")


## click relative location
x, y = wa.get_relative_location(root, child)
wa.click_relative_location(root, x, y)


## click absolute location
wa.click_at(38, 864, visible=False)
# wa.click_at(4501, 1394, visible=True)




## Image feature matching
import pyautomation.pyautovision as vs
min_match_count=15
template_path= r".\imgs\fcfb.jpg"

a = vs.main(min_match_count=min_match_count, template_path=template_path, show=False)
print(a.object_center, a.object_location)


## click from image
wa.click_at(a.object_center[0], a.object_center[1], visible=False)


## monitor info
import pyautomation.displayinfo as pydis
print(pydis.DisplayInfo().get_scale_factor(pydis.DisplayInfo().get_Qapp()))
print(pydis.DisplayInfo().get_screen_info())