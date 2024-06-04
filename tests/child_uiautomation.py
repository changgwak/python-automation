import msuiauto as auto
import time

time.sleep(2)

desired_parent_name = "child_uiautomation.py - python-autoevent - Visual Studio Code"
desired_child_name = "GitLens Inspect"
root = auto.PaneControl(Name=desired_parent_name)
# desired_parent_name = "*Readme.txt - 메모장"
# desired_child_name = "텍스트 편집기"
# root = auto.WindowControl(Name=desired_parent_name)


def get_info(control, depth=0, delimiter=""):
    try:
        child_handle = control.NativeWindowHandle
        child_name = control.Name
        child_controltype = control.LocalizedControlType
        child_location = control.BoundingRectangle
        child_classname = control.ClassName
        print(f"{delimiter} Depth: {depth}, Window Handle: {child_handle}, name: {child_name}, control_type: {child_controltype}, location: {child_location}, classname: {child_classname}")
    except Exception as e:
        print(e)


def get_relative_location(parent_control, child_control):
    try:
        parent_rectangle = parent_control.BoundingRectangle
        child_rectangle = child_control.BoundingRectangle
        print(parent_rectangle, child_rectangle)

        parent_x = parent_rectangle.left
        parent_y = parent_rectangle.top
        child_x = child_rectangle.left
        child_y = child_rectangle.top

        # # 요소의 상대 좌표 계산
        relative_x = child_x - parent_x
        relative_y = child_y - parent_y

        # print(f"요소의 상대 좌표: ({relative_x}, {relative_y})")

        # # # 요소의 중앙 좌표 계산
        center_x = child_x + (child_rectangle.width() // 2)
        center_y = child_y + (child_rectangle.height() // 2)

        # 앱 창에 대한 상대 중앙 좌표
        relative_center_x = center_x - parent_x
        relative_center_y = center_y - parent_y

        # print(relative_center_x, relative_center_y)

        return relative_center_x, relative_center_y
    except Exception as e:
        print(e)
    


get_info(root, delimiter="root")

## FirstChildControl 메소드는 첫 번째 자식 컨트롤을 찾습니다.
first_child = root.GetFirstChildControl()
get_info(first_child, delimiter="first_child")

## LastChildControl 메소드는 마지막 자식 컨트롤을 찾습니다.
last_child = root.GetLastChildControl()
get_info(last_child, delimiter="last_child")


## WalkControl 메소드는 트리를 순회하며 조건에 맞는 컨트롤을 찾습니다.
cnt=0
def walk_and_find(control, condition=None, depth=0):
    global cnt
    if condition(control):
        return control, depth  # 조건에 맞는 컨트롤과 현재 깊이 반환
    for child in control.GetChildren():
        get_info(child, depth, "**child")  # 깊이 정보를 get_info 함수로 전달
        cnt += 1
        result, result_depth = walk_and_find(child, condition, depth+1)  # 깊이를 1 증가시키고 자식 컨트롤 탐색
        if result:
            return result, result_depth
    return None, None  # 조건에 맞는 컨트롤을 찾지 못한 경우

child, child_depth = walk_and_find(root, lambda c: c.Name == desired_child_name)
get_info(child, child_depth, "Target")
get_info(child.GetParentControl(), child_depth-1, "Target Parent")
x,y= get_relative_location(root, child)
print(x,y)
print("###############")
print(cnt)
# edit = root.TabItemControl(searchDepth = 13, Name= desired_child_name) # Name= "삽입"
# get_info(edit, "edit")


def walk_and_find_all(control, condition=None, depth=0):
    global cnt
    found_controls = []
    if condition is None:
        condition = lambda x: True  # 조건이 None이면 모든 컨트롤을 반환합니다.

    if condition(control):
        found_controls.append((control, depth))  # 컨트롤과 깊이 정보를 함께 추가

    for child in control.GetChildren():
        cnt += 1
        get_info(child, depth, "****child")  # 깊이 정보를 함께 출력하도록 get_info 함수 수정 필요

        # 재귀적으로 자식 컨트롤 탐색, 깊이를 1 증가시킴
        found_controls.extend(walk_and_find_all(child, condition, depth + 1))

    return found_controls

# print("###############")
# child = walk_and_find_all(root, condition=None)
# print("###############")
# print(cnt)

import win32gui, win32con, win32api
def click_relative_location(parent_control, x, y):
    hWnd = parent_control.NativeWindowHandle
    lParam = win32api.MAKELONG(x, y)
    win32gui.PostMessage(hWnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    win32gui.PostMessage(hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32api.Sleep(100) #ms
    win32gui.PostMessage(hWnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)
    # win32api.Sleep(100) #ms
    # win32gui.PostMessage(hWnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    # win32gui.PostMessage(hWnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

def click_direct_child(child_control) :
    hwnd = child_control.NativeWindowHandle
    win32gui.PostMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
    # win32api.Sleep(100) #ms
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)

def type_text(hwnd, text):
    for char in text:
        if char == "\n":
            # Enter event
            win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        else:
            win32gui.PostMessage(hwnd, win32con.WM_CHAR, ord(char), 0)


# click_relative_location(root, x, y)
# click_direct_child(child)
# type_text(child, "test type text") ## 



## GetChildren 메소드는 모든 자식 컨트롤을 반환합니다.
children = root.GetChildren()
for child in children:
    get_info(child, 0, "GetChildren")

## TabItemControl 메소드는 탭 항목을 찾습니다.
# tab_item = root.DocumentControl(Name=desired_child_name) #"Settings"
# tab_item_handle = tab_item.NativeWindowHandle
# print(f"Document Handle: {tab_item_handle}")

# ## TabItemControl 메소드는 탭 항목을 찾습니다.
# tab_item = root.TabItemControl(Name=desired_child_name) #"Settings"
# tab_item_handle = tab_item.NativeWindowHandle
# print(f"Tab Item Handle: {tab_item_handle}")

# ## ToolBarControl 메소드는 툴바를 찾습니다.
# toolbar = root.ToolBarControl(Name=desired_child_name)
# toolbar_handle = toolbar.NativeWindowHandle
# print(f"Toolbar Handle: {toolbar_handle}")

# ## EditControl 메소드는 텍스트 입력 상자를 찾습니다.
# edit_control = root.EditControl(Name=desired_child_name)
# edit_control_handle = edit_control.NativeWindowHandle
# print(f"Edit Control Handle: {edit_control_handle}")

# ## MenuItemControl 메소드는 메뉴 항목을 찾습니다.
# menu_item = root.MenuItemControl(Name="File")
# menu_item_handle = menu_item.NativeWindowHandle
# print(f"Menu Item Handle: {menu_item_handle}")

# ## TextControl 메소드는 텍스트 컨트롤을 찾습니다.
# text_control = root.TextControl(Name="WelcomeMessage")
# text_control_handle = text_control.NativeWindowHandle
# print(f"Text Control Handle: {text_control_handle}")





## AndCondition 메소드는 여러 조건을 모두 만족하는 컨트롤을 찾습니다.
# condition = auto.AndCondition(auto.ControlTypeCondition(auto.ControlType.Edit), auto.NameCondition("Username"))
# edit_control = root.FindControl(condition)
# edit_control_handle = edit_control.NativeWindowHandle
# print(f"Edit Control Handle: {edit_control_handle}")

## OrCondition 메소드는 여러 조건 중 하나라도 만족하는 컨트롤을 찾습니다.
# condition = auto.OrCondition(auto.ControlTypeCondition(auto.ControlType.Edit), auto.NameCondition("Username"))
# control = root.FindControl(condition)
# control_handle = control.NativeWindowHandle
# print(f"Control Handle: {control_handle}")

## WaitForExist 메소드는 특정 컨트롤이 나타날 때까지 기다립니다.
# control = auto.WaitForExist(lambda: root.FindControl(Name=desired_child_name), timeout=10)
# control_handle = control.NativeWindowHandle
# print(f"Child Window Handle: {control_handle}")

# ## WaitForDisappear 메소드는 특정 컨트롤이 사라질 때까지 기다립니다.
# auto.WaitForDisappear(lambda: root.FindControl(Name=desired_child_name), timeout=10)
# print("Control has disappeared.")


# ## GetParent 메소드는 부모 컨트롤을 찾습니다.
# parent = some_control.GetParent()
# parent_handle = parent.NativeWindowHandle
# print(f"Parent Window Handle: {parent_handle}")

# ## GetNextSibling 메소드는 다음 형제 컨트롤을 찾습니다.
# next_sibling = some_control.GetNextSibling()
# next_sibling_handle = next_sibling.NativeWindowHandle
# print(f"Next Sibling Window Handle: {next_sibling_handle}")

# ## GetPreviousSibling 메소드는 이전 형제 컨트롤을 찾습니다.
# previous_sibling = some_control.GetPreviousSibling()
# previous_sibling_handle = previous_sibling.NativeWindowHandle
# print(f"Previous Sibling Window Handle: {previous_sibling_handle}")

# ## NextSiblingControl 메소드는 다음 형제 컨트롤을 찾습니다.
# next_sibling = some_control.NextSiblingControl()
# next_sibling_handle = next_sibling.NativeWindowHandle
# print(f"Next Sibling Window Handle: {next_sibling_handle}")

# ## PreviousSiblingControl 메소드는 이전 형제 컨트롤을 찾습니다.
# previous_sibling = some_control.PreviousSiblingControl()
# previous_sibling_handle = previous_sibling.NativeWindowHandle
# print(f"Previous Sibling Window Handle: {previous_sibling_handle}")


# # WaitForControl 메소드는 특정 조건을 만족하는 컨트롤이 나타날 때까지 기다립니다.
# control = root.WaitForControl(Name=desired_child_name, timeout=10)
# control_handle = control.NativeWindowHandle
# print(f"Child Window Handle: {control_handle}")