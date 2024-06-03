from ..pyautomation import pyauto


desired_parent_name = "pyauto.py - python-autoevent - Visual Studio Code"
desired_child_name = "GitLens Inspect"

wa = pyauto.WinAuto(desired_parent_name, desired_child_name)
root = pyauto.msauto.PaneControl(Name=desired_parent_name)

child, child_depth = wa.walk_and_find(root)
wa.get_info(child, child_depth, "Target")
wa.get_info(child.GetParentControl(), child_depth-1, "Target Parent")