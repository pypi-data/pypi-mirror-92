import sys
from os import path
from setuptools import setup
from tkpick import about as a


setupdir = path.dirname(__file__)

if sys.version_info < (3, 5):
    raise RuntimeError("Tkpick requires Python 3.5 or later")

with open(path.join(setupdir, "README.md"), encoding="ASCII") as f:
    long_description = f.read()


setup(
    name="tkpick",
    version=a.__version__,
    packages=["tkpick"],
    description=a.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=a.__source__,
    author=a.__author__,
    author_email=a.__contact__,
    license="GPL-3.0",
    classifiers=[
        "Topic :: Utilities",
        "Natural Language :: English",
        "Topic :: Multimedia :: Graphics",
        "Environment :: X11 Applications",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Environment :: X11 Applications :: GTK",
    ],
    platforms=["Linux"],
    python_requires=">=3.5",
    install_requires=["pynput", "PyGObject"],
    keywords=["tkinter", "pick", "cursor", "pixel", "color"],
    package_data={"tkpick": ["assets/*.*"]},
    data_files=[
        ("share/applications", ["tkpick.desktop"]),
        ("share/icons", ["tkpick/assets/tkpick.png"]),
    ],
    entry_points={
        "gui_scripts": ["tkpick = tkpick:main", "Tkpick = tkpick:main"],
    },
)
