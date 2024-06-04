# pyautomation

pyautomation is a set of Python modules designed to automate the Microsoft Windows GUI, specifically without interacting with the mouse cursor and keyboard. At its simplest, it allows you to post mouse and keyboard events to Windows dialogs and controls.

With the pyautomation package, you can control your GUI automatically while simultaneously controlling the mouse and keyboard physically, similar to how selenium automates web browsers.

### Create virtual environment(optional)

```bash
python -m venv myvenv
```
```bash
source ./myvenv/Scripts/activate
```

### Installation

```bash
pip install pyautomation
```

### How to use
```python
import pyautomation

```

### Download inspect.exe
https://learn.microsoft.com/en-us/windows/win32/winauto/inspect-objects



## How to update PYPI

### Revision codes
1. Update on Github after modifying codes.

### Update version

1. package 내 `__init__.py` 에서 `__version__`파일 업데이트
2. `setup.py` 내 `version` 업데이트(1번과 동일하게 설정)
3. `setup.py` 내 `install_requires`가 추가된 경우 추가 후 업데이트

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
