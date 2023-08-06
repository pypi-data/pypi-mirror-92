# setup.py

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="nlpaeg",
    version="0.0.6",
    description="Artificial Error Generation (AEG) for Natural Language Processing",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/praveentn/nlpaeg",
    author="Praveen Narayan",
    author_email="sigmoidptn@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["nlpaeg"],
    include_package_data=True,
    install_requires=["numpy", "pandas", "lemminflect"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)