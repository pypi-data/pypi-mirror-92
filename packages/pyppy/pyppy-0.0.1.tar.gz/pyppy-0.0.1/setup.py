import os
import setuptools


PATH_TO_THIS_SCRIPT = os.path.abspath(os.path.dirname(__file__))


setuptools.setup(
    name="pyppy",
    version="0.0.1",
    author="David Grimm",
    author_email="mail@david-grimm.de",
    description="pyppy",
    packages=setuptools.find_packages(PATH_TO_THIS_SCRIPT),
    python_requires='>=3.8'
)
