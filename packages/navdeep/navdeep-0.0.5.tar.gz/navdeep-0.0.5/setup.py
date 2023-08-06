
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="navdeep", # Replace with your own username
    version="0.0.5",
    author="Navdeep",
    author_email="sujith133@gmail.com",
    description="lets you know if given int is prime or odd or even",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Navdeep6/tpackage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
