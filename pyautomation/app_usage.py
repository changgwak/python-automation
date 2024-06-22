



import pyautovision
min_match_count=15
template_path= r"..\python-automation\tests\imgs\fcfb.jpg"

a = pyautovision.main(min_match_count=min_match_count, template_path=template_path, show=False)
print(a.object_center, a.object_location)



import pyauto

def app_module():
    return print("this is app_module function")





# Sample usage of WinAuto methods
def main():
    ## Load configuration
    # config_path = r'pyautomation\config\pyauto.json'
    # config = pyauto.ConfigLoader.load_config(config_path)
    config = pyauto.ConfigLoader.load_config(desired_parent_name= "app_usage.py - python-autoevent - Visual Studio Code", desired_child_name= "Docker", monitor_index=1)
    # config = pyauto.ConfigLoader.load_config()

    wa = pyauto.WinAuto(config=config)


    # root = pyauto.msauto.PaneControl(Name=config.desired_parent_name)

    # child, child_depth = wa.walk_and_find(root)
    # wa.get_info(child, child_depth, "Target")
    # wa.get_info(child.GetParentControl(), child_depth-1, "Target Parent")
    

    ## click relative location
    # x, y = wa.get_relative_location(root, child)
    # wa.click_relative_location(root, x, y)
 

    ## click from image or absolute location
    wa.click_at(a.object_center[0], a.object_center[1], visible=False)
    
    # wa.click_at(38, 864, visible=False)
    # wa.click_at(4501, 1394, visible=True)



    ## Handle Usage
    # import os, time
    # os.system ('notepad.exe')
    # time.sleep(3)
    # window = pyauto.msauto.WindowControl(searchDepth=1, ClassName='Notepad')

    # config = pyauto.ConfigLoader.load_config(desired_parent_name= window.Name, desired_child_name= "Text editor")
    # wa = pyauto.WinAuto(config=config)
    # result, depth = wa.walk_and_find(window)
    # wa.type_text(result.NativeWindowHandle, "hello notepad!")

if __name__ == "__main__":
    main()




# import displayinfo as pydis
# print(pydis.DisplayInfo().get_scale_factor(pydis.DisplayInfo().get_Qapp()))
# print(pydis.DisplayInfo().get_screen_info())



