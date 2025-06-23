# setup.py
# Setup script for Haven Bot

from setuptools import setup, find_packages

setup(
    name="havenbot",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "web3",
        "requests",
        "python-dotenv",
        "pandas",
        "numpy",
    ],
)