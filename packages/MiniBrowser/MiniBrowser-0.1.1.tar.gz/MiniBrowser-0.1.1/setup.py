import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MiniBrowser",
    version="0.1.1",
    author="Hugo van de Kuilen from Hugo4IT.com",
    author_email="hugo.vandekuilen1234567890@gmail.com",
    description="A WIP mini browser for python. Don't expect much from this",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hugo4IT/PythonEventSystem",
    packages=setuptools.find_packages(),
    install_requires=[
        'PygameUILib',
        'pygame'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
