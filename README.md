# 테스트용 패키지

테스트

### 설치(installation)

```bash
pip install pyautomation
```

### 데이터셋 리스트 확인

```python
from autoevent

[function]
```

## PYPI 업데이트 방법

### 코드 수정
1. 코드 수정 후 Github에 업데이트

### 버전 업데이트

1. package 내 `__init__.py` 에서 `__version__`파일 업데이트
2. `setup.py` 내 `version` 업데이트(1번과 동일하게 설정)
3. `setup.py` 내 `install_requires`가 추가된 경우 추가 후 업데이트

### whl 파일 생성
```bash
python setup.py sdist bdist_wheel
python setup.py bdist_wheel
```

> whl 파일 업로드
```bash
python -m twine upload dist/*
twine upload dist/pyautomation-X.X.X-py3-none-any.whl
```
