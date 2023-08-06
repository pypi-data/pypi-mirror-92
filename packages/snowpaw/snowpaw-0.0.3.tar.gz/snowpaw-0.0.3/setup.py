import setuptools
from io import open

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snowpaw",
    version="0.0.3",
    author="Liu Jianwei",
    author_email="tungliu@126.com",
    description="A useful python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://lttpp.github.io/snowpaw/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
