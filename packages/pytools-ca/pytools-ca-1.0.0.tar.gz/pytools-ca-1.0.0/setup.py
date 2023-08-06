import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytools-ca",
    version="1.0.0",
    author="cmplxapps",
    author_email="cmplxapps@gmail.com",
    description="Just a collection of useful tools to make coding a bit easier.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://cmplxapps.github.io",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)