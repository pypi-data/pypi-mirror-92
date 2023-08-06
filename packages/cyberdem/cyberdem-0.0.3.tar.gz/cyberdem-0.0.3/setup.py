import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf8")
LICENSE = (HERE / "LICENSE.md").read_text(encoding="utf8")

setup(
    name="cyberdem",
    version="0.0.3",
    description="CyberDEM SISO standard python helper package",
    long_description="CyberDEM SISO standard python helper package",
    #long_description=README,
    #long_description_content_type="text/markdown",
    author="Carnegie Mellon University",
    url="https://github.com/cmu-sei/cyberdem-python",
    license=LICENSE,
    platforms=['any'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
)
