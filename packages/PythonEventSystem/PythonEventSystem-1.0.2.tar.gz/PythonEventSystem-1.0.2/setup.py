import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PythonEventSystem",
    version="1.0.2",
    author="Hugo van de Kuilen from Hugo4IT.com",
    author_email="hugo.vandekuilen1234567890@gmail.com",
    description="An easy-to-use pygame User Interface Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hugo4IT/PythonEventSystem",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
