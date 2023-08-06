import pathlib
from pathlib import Path
from setuptools import setup
import os

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

if not os.path.exists(f'{str(Path.home())}/.cheatsheets/'):
    os.makedirs(f'{str(Path.home())}/.cheatsheets/')

setup(
    name="cheatsheets",
    version="0.0.1",
    description="Cheatsheets",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Tlalocan/cheatsheets",
    author="Tlaloc-Es",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["cheatsheets"],
    include_package_data=True,
    install_requires=["simple-term-menu", "pygments"],
    entry_points={
        "console_scripts": [
            "cheatsheets=cheatsheets.cheatsheets:main",
        ]
    },
)