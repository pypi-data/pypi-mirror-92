import pathlib

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="dearpygui-wrapper",
    version="0.0.1",
    description="A Pythonic UI wrapper library for DearPyGui ",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/adamgilman/dearpygui-wrapper",
    author="Adam Gilman",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["dearpygui-wrapper"],
    include_package_data=True,
    install_requires=["dearpygui"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)
