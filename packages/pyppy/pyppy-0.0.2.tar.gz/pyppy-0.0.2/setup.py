import os
import setuptools


PATH_TO_THIS_SCRIPT = os.path.abspath(os.path.dirname(__file__))


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyppy",
    version="0.0.2",
    author="David Grimm",
    author_email="maehster@gmail.com",
    description="Python library for global configuration and conditional method execution.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maehster/pyppy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)