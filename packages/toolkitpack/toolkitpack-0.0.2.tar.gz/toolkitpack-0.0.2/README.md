# toolkit-pack

This is an example project demonstrating how to publish a python module to PyPI

## Installation

Run the following to install:

```python
pip install toolkitpack
```

## Usage

```python
from toolkitFile import add

# Add two numbers
add(5, 10)
```

## Steps to make your own

[This guy taught me](https://youtu.be/GIF3LaRqgXo)

- Add your python code to src folder, the directory should look something like this

  ![img](tree.png)

- Create a setup.py file in the same location as src folder

  - Add necessary configurations in setup.py, like

  ```python
  # Don't use distutils, setup comes with Python in setuptools
    from setuptools import setup

    setup(
    name='toolkitpack',
    version='0.0.1',
    description='Random operations who cares',
    py_modules=['tookitFile', 'additionalFiles'],
    package_dir={'': 'src'},
  )

  ```

- Let's create a wheel file (format in which we upload to PyPi)

  ```bash

  python setup.py bdist_wheel
  ```

  Don't be alarmed as this command will generate a lot of additional files

- Install package locally using Pip

  ```bash
  pip install -e .
  ```

- After making sure everything is working perfectly lets bind everything together

  ```bash

  python setup.py bdist_wheel sdist
  ```

- Now to upload our packages to PyPI index we need a tool named twine. Install it using the following command

  ```bash
  pip install twine
  ```

  Now upload the files in dist folder, it will ask for username and password

  ```bash
  twine upload dist/*
  ```
