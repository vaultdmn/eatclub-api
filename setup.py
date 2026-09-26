from setuptools import setup, find_packages

setup(
    name="eatclub",
    version="0.1.0",
    description="Python API Client for EatClub (Box8)",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0"
    ],
    author="Claude",
    python_requires=">=3.7",
)
