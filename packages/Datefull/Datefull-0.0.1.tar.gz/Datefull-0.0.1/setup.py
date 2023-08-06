import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Datefull",
    version="0.0.1",
    author="irakli googoochani",
    author_email="irakligoogoochaniv@gmail.com",
    description="Use module for your program",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/33f44",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)

