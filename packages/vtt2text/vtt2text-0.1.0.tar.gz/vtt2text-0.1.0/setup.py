# -*- coding: utf-8 -*-
# @Author: anh-tuan.vu
# @Date:   2021-01-27 10:29:59
# @Last Modified by:   anh-tuan.vu
# @Last Modified time: 2021-01-27 15:28:59

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "vtt2text",
    version = "0.1.0",
    author = "VU Anh Tuan",
    author_email = "vuanhtuan1012@outlook.com",
    description = "A small package to clean up the content of a subtitle file to text",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/vuanhtuan1012/vtt2text",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.6',
)