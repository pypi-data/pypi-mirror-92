from setuptools import setup,find_packages
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="UiComparePicRec",
    version="1.1.0",
    author="Jishuang Li",
    author_email="1103192570@qq.com",
    description="Selenium plugin library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lijishuang/UI-Pic-Rec",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
)

