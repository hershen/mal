from setuptools import setup

setup(
    name="malPython",
    version="0.1",
    author="Alon Hershenhorn",
    author_email="hershen@gmail.com",
    description=(
        "An implementation of the list-like programming language mal in Python3."
    ),
    install_requires=['readline'],
    entry_points={"console_scripts":"mal=malPython.stapA_mal:main"},
    url="https://github.com/hershen/mal/tree/master/impls/myPython",
    python_requires='~=3.6',
    packages=["malPython"],
)
