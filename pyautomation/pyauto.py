import msuiauto as msauto
import win32gui, win32con, win32api

class WinAuto() :
    def __init__(self, desired_parent_name="", desired_child_name=""):
        self.desired_parent_name = desired_parent_name
        self.desired_child_name = desired_child_name
        # self.msauto = msuiauto()

    def get_info(self, control, depth=0, delimiter=""):
        try:
            child_handle = control.NativeWindowHandle
            child_name = control.Name
            child_controltype = control.LocalizedControlType
            child_location = control.BoundingRectangle
            child_classname = control.ClassName
            print(f"{delimiter} Depth: {depth}, Window Handle: {child_handle}, name: {child_name}, control_type: {child_controltype}, location: {child_location}, classname: {child_classname}")
        except Exception as e:
            print(e)


    def get_relative_location(self, parent_control, child_control):
        try:
            parent_rectangle = parent_control.BoundingRectangle
            child_rectangle = child_control.BoundingRectangle
            # print(parent_rectangle, child_rectangle)

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
    


    def walk_and_find(self, control, depth=0):
        # global cnt
        
        condition = lambda c: c.Name == self.desired_child_name
        if condition(control):
            return control, depth  # 조건에 맞는 컨트롤과 현재 깊이 반환
        for child in control.GetChildren():
            self.get_info(child, depth, "**child")  # 깊이 정보를 get_info 함수로 전달
            # cnt += 1
            result, result_depth = self.walk_and_find(child, depth+1)  # 깊이를 1 증가시키고 자식 컨트롤 탐색
            if result:
                return result, result_depth
        return None, None  # 조건에 맞는 컨트롤을 찾지 못한 경우
    

    def walk_and_find_all(self, control, condition=None, depth=0):
        # global cnt
        found_controls = []
        if condition is None:
            condition = lambda x: True  # 조건이 None이면 모든 컨트롤을 반환합니다.

        if condition(control):
            found_controls.append((control, depth))  # 컨트롤과 깊이 정보를 함께 추가

        for child in control.GetChildren():
            # cnt += 1
            self.get_info(child, depth, "****child")  # 깊이 정보를 함께 출력하도록 get_info 함수 수정 필요

            # 재귀적으로 자식 컨트롤 탐색, 깊이를 1 증가시킴
            found_controls.extend(self.walk_and_find_all(child, condition, depth + 1))

        return found_controls
    




    def click_relative_location(self, parent_control, x, y):
        hWnd = parent_control.NativeWindowHandle
        lParam = win32api.MAKELONG(x, y)
        win32gui.PostMessage(hWnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        win32gui.PostMessage(hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32api.Sleep(100) #ms
        win32gui.PostMessage(hWnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)
        # win32api.Sleep(100) #ms
        # win32gui.PostMessage(hWnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        # win32gui.PostMessage(hWnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

    def click_direct_child(self, child_control) :
        hwnd = child_control.NativeWindowHandle
        win32gui.PostMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
        # win32api.Sleep(100) #ms
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)

    def type_text(self, hwnd, text):
        for char in text:
            if char == "\n":
                # 엔터 키 처리
                win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
            else:
                win32gui.PostMessage(hwnd, win32con.WM_CHAR, ord(char), 0)


    def get_all_children(self, root):
        ## GetChildren 메소드는 모든 자식 컨트롤을 반환
        children = root.GetChildren()
        for child in children:
            self.get_info(child, 0, "GetChildren")





