from setuptools import setup

import sys

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

setup(
    name="mal_python",
    version="1.1",
    author="Alon Hershenhorn",
    author_email="hershen@gmail.com",
    description=(
        "An implementation of the lisp-like programming language mal in Python3."
    ),
    long_description=(
        "This is an implementation of the lisp-like programming langauge mal.\nIt is implemented in Python3."
    ),
    install_requires=[
        'readline; platform_system == "Linux"',
        'pyreadline; platform_system == "Windows"',
    ],
    entry_points={"console_scripts": "mal=mal_python.stepA_mal:main"},
    url="https://github.com/hershen/mal/tree/master/impls/myPython",
    python_requires=">=3.6",
    packages=["mal_python"],
)
