from pathlib import Path
from setuptools import setup, find_packages

# The directory containing this file
HERE = Path(__file__).parent.resolve()
open(str(HERE/'validdocbr.py'))

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="validdocbr",
    version="1.2.2",
    description="Brazilian document validator using the check digit",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/JohnChinaski/validdocbr",
    author="johnchinaski",
    author_email="joao.pog90@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,    
    entry_points={
        "console_scripts": [
            "validdocbr=validdocbr.__main__:main",
        ]
    },
)
