# pypi-hellow-word

1. Ensure pipi, setuptools, and wheel are up to date
```
python -m pip install --upgrade pip setuptools wheel
```

```
python setup.py sdist bdist_wheel
```
```
python -m pip install --upgrade twine
```
```
python -m twine upload --repository testpypi dist/*
```