# pypi-hellow-word

## 1. Ensure pipi, setuptools, and wheel are up to date
```
python -m pip install --upgrade pip setuptools wheel
```
## 2. Build and Push it
```
python setup.py sdist bdist_wheel
```
```
pip install -e .
```
```
python -m pip install --upgrade twine
```

```
twine upload dist/*
```
## 3. Auth your account
- **username**: mcanv
- **password**: **********