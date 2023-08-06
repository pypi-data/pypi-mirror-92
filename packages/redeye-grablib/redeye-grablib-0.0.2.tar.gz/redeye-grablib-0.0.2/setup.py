import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="redeye-grablib",
    version="0.0.2",
    author="CMSteffen",
    author_email="cmsteffen@haxys.net",
    description="A library for retrieving files from HTTP servers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RedEyeApp/grablib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "requests",
    ],
)
