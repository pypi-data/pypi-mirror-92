# Hello World

## 1. Ensure pip, setuptools, and wheel are up to date
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



This is an example project demonstrating how to publish a python module to PyPI.

## Installation

Run the following to install:

```
python pip install helloworld-mcv
```

## Usage

```
from helloworld import say_hello

# Generate "Hello, World!"
say_hello()

# Generate "Hello, Everybody!"
say_hello("Everybody")
```