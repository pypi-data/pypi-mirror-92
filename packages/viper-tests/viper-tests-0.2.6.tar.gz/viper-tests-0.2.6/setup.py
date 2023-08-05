from setuptools import setup
import os

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, "README.md")) as readme:
    longDescription = readme.read()

setup(
    name = "viper-tests",
    version = "0.2.6",
    description = "A modern testing framework",
    long_description = longDescription,
    long_description_content_type = "text/markdown",
    keywords = ["tests", "testing", "unittest", "viper"],
    author = "Aarush Gupta",
    author_email = "hello@aarushgupta.tk",
    packages = ["viper"],
    package_data = {},
    install_requires = ["colorama"],
    python_requires = ">=3.6"
)