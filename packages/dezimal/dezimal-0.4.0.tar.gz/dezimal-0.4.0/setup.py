import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dezimal",
    version="0.4.0",
    author="Julian Fleischer",
    author_email="tirednesscankill@warhog.net",
    description="Arbitrary precision decimal numbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scravy/dezimal-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Typing :: Typed",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires='>=3.6',
)
