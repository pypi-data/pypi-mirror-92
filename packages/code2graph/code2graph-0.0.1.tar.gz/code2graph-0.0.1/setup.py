import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="code2graph",
    version="0.0.1",
    author="Ali Varfan",
    description="A package for creating directed graph from python files",
    long_description="This program will recursively search a path, finds all the python files and extracts a directed graph from them to show which functions is calling/using which other function and class",
    long_description_content_type="text/markdown",
    url="https://gitlab.com/avarf/code2graph",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)