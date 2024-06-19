
# import pyauto

# def app_module():
#     return print("this is app_module function")


# # Load configuration
# config_path = r'pyautomation\config\pyauto.json'
# config = pyauto.ConfigLoader.load_config(config_path)

# # Initialize WinAuto with configuration
# win_auto = pyauto.WinAuto(config=config)

# # Sample usage of WinAuto methods
# def main():
#     wa = pyauto.WinAuto(config)
#     root = pyauto.msauto.PaneControl(Name=config.desired_parent_name)

#     child, child_depth = wa.walk_and_find(root)
#     wa.get_info(child, child_depth, "Target")
#     wa.get_info(child.GetParentControl(), child_depth-1, "Target Parent")
    
 
# if __name__ == "__main__":
#     main()




# import displayinfo as pydis
# print(pydis.DisplayInfo().get_scale_factor(pydis.DisplayInfo().get_Qapp()))
# print(pydis.DisplayInfo().get_screen_info())



import pyautovision
a = pyautovision.main(r'config/autovision.yaml')
print(a.object_center, a.object_location)