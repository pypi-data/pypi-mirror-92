import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrror",
    version="0.0.4",
    author="Dacker",
    author_email="hello@dacker.co",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dacker-team/pyrror",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    install_requires=[
        "requests>=2.22.0",
        "pandas==1.0.3",
        "pyyaml==5.3.1"
    ],
)
