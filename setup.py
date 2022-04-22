from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="tark",
    version="0.0.1",
    author="tyler jones",
    description="Markdown parser focused on blogs.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/tylerhjones/tark/",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
)