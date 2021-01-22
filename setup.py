import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pyhunterdouglasplatinum",
    version="1.0.1",
    description="Python library to talk to Hunter Douglas Platinum Hubs",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/schwark/pyhunterdouglasplatinum",
    author="Schwark Satyavolu",
    author_email="schwark@alum.rpi.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["hunterdouglasplatinum"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pyhunterdouglasplatinum=hunterdouglasplatinum.__main__:main",
        ]
    },
)
