import os
import setuptools


PATH_TO_THIS_SCRIPT = os.path.abspath(os.path.dirname(__file__))


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyppy",
    version="0.1.0",
    author="David Grimm",
    author_email="maehster@gmail.com",
    description="Python library for global configuration and conditional method execution.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maehster/pyppy",
    packages=setuptools.find_packages(PATH_TO_THIS_SCRIPT),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
    extras_require={
        'dev': [
            'pytest',
            'pytest-pep8',
            'pytest-cov',
            'pylint>=2.6.0'
        ]
    }
)
