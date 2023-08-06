from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='toolkitpack',
    version='0.0.2',
    description='Random operations who cares',
    url="https://github.com/asishRye/package",
    author="Asish Binu Mathew",
    author_email="asish+pypi@accubits.com",
    py_modules=['toolkitFile', 'additionalFiles'],
    package_dir={'': 'src'},
    classifiers=["Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.7"],
    long_description=long_description,
    long_description_content_type="text/markdown",

    install_requires=[
        "blessings==1.7",
    ],
    extra_require={
        "dev": [
            "pytest>=3.7",
        ]
    },
)
