import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="code2graph",
    version="0.0.2",
    author="Ali Varfan",
    description="A package for creating directed graph from python files",
    scripts = ["code2graph/code2graph.py"],
    long_description=long_description,
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