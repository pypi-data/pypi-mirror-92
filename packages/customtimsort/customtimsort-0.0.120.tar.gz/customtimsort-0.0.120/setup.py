import os
import sys
import platform
from os import listdir
from sysconfig import get_paths
from os.path import isfile, join
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

PATH = get_paths()["include"]


def create_file_with_includes():
    files = [file for file in listdir(PATH) if isfile(join(PATH, file))]
    with open("all_headers.h", 'w') as f:
        for file in files:
            if file not in ["pyexpat.h", "py_curses.h", "graminit.h"]:
                f.write(f"#include <{file}>" + "\n")

create_file_with_includes()

setuptools.setup(
    name='customtimsort',
    version='0.0.120',
    author='lehatr',
    author_email='lehatrutenb@gmail.com',
    description="Timsort sorting algorithm with custom minrun",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    ext_modules=[
        setuptools.Extension("timsort",
            sources=["timsort.c", "listobject.c"],
            include_dirs=[
                os.path.join(os.getcwd(), ''),
                PATH,
            ],
            language='c',
        )
    ]
)
