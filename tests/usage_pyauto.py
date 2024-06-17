import os
import json
from pyauto import ConfigLoader, WinAuto

# Load configuration
config_path = 'config.json'
config = ConfigLoader.load_config(config_path)

# Initialize WinAuto with configuration
win_auto = WinAuto(config=config)

# Sample usage of WinAuto methods
def main():
    # Example: Click at a specific location (150, 30) with visibility and scale factor
    win_auto.click_at(150, 30, visible=True, scale_factor=1.5)
    
    # Example: Get relative location of child control to parent control
    class MockControl:
        def __init__(self, left, top, right, bottom):
            self.BoundingRectangle = self.Rectangle(left, top, right, bottom)
        class Rectangle:
            def __init__(self, left, top, right, bottom):
                self.left = left
                self.top = top
                self.right = right
                self.bottom = bottom
            def width(self):
                return self.right - self.left
            def height(self):
                return self.bottom - self.top

    parent_control = MockControl(10, 10, 100, 100)
    child_control = MockControl(20, 20, 40, 40)
    relative_x, relative_y = win_auto.get_relative_location(parent_control, child_control)
    print(f"Relative location: ({relative_x}, {relative_y})")

    # Example: Click at a relative location within the parent control
    win_auto.click_relative_location(parent_control, 30, 30)

    # Example: Walk and find a control by name
    class MockControlWithName(MockControl):
        def __init__(self, name, children=[]):
            super().__init__(0, 0, 100, 100)
            self.Name = name
            self._children = children
        def GetChildren(self):
            return self._children

    desired_child = MockControlWithName(config.desired_child_name)
    root_control = MockControlWithName("root", [desired_child])
    
    found_control, depth = win_auto.walk_and_find(root_control)
    if found_control:
        print(f"Found control: {found_control.Name} at depth {depth}")
    else:
        print("Desired control not found")

    # Example: Schedule a task using a cron expression (every minute)
    win_auto.schedule_task(lambda: win_auto.click_at(150, 30), '* * * * *')

if __name__ == "__main__":
    main()
