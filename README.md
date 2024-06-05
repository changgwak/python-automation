# pyautomation

pyautomation is a set of Python modules designed to automate the Microsoft Windows GUI, specifically without interacting with the mouse cursor and keyboard. At its simplest, it allows you to post mouse and keyboard events to Windows dialogs and controls.

With the pyautomation package, you can control your GUI automatically while simultaneously controlling the mouse and keyboard physically, similar to how selenium automates web browsers.

### Create virtual environment(Recommended)

```bash
python -m venv myvenv
```
```bash
source ./myvenv/Scripts/activate
```

### Installation

```bash
pip install python-automation
```

### How to use
```python
import os
import time

import pyautomation.msuiauto as auto
import pyautomation.pyauto as pyapp


os.system ('notepad.exe')
time.sleep(5)
window = auto.WindowControl(searchDepth=1, ClassName='Notepad')
pyauto = pyapp.WinAuto(window.Name, "Text Editor")
# pyauto = pyapp.WinAuto(window.Name, "텍스트 편집기")
result, depth = pyauto.walk_and_find(window)
pyauto.type_text(result.NativeWindowHandle, "hello notepad!")

import pyautomation.displayinfo as pydis
print(pydis.DisplayInfo().get_scale_factor(pydis.DisplayInfo().get_Qapp()))
print(pydis.DisplayInfo().get_screen_info())

```

### How to download inspect.exe
Click this [git repo](https://github.com/changgwak/python-automation/tree/master/inspect) or [MS Official Website for inspect](https://learn.microsoft.com/en-us/windows/win32/winauto/inspect-objects)  




## How to update PYPI (for only project manager)

### Revision codes
1. Update on Github after modifying codes.

### Update version

1. Update `__version__` in `__init__.py` file in package
2. Update `version` in `setup.py` file (Same setting as first step)
3. Update after addtion, if `install_requires` is added in `setup.py`

### Generate whl file
```bash
python setup.py sdist bdist_wheel
python setup.py bdist_wheel
```

> Upload whl file
```bash
python -m twine upload dist/*
twine upload dist/pyautomation-X.X.X-py3-none-any.whl
```
