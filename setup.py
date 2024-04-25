from setuptools import setup, find_packages

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setup(
    name="mathchords",
    version="1.0.0",
    author="Santiago Angarita",
    author_email="hsangaritaga@unal.edu.co",
    description="A package for mathematical operations on musical chords",
#    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hsmathang/mathchords",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)