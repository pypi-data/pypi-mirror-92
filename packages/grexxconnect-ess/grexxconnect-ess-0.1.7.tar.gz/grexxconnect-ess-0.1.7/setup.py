import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="grexxconnect-ess",
    version="0.1.7",
    description="Grexx External System Service Helper",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Grexx",
    author_email="servicedesk@grexx.net",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    install_requires=["websockets", "colorlog"],
)
