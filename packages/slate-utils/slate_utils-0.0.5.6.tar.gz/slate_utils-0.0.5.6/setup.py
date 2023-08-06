from setuptools import find_packages, setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="slate_utils",
    version="0.0.5.6",
    author="Jamie Davis",
    author_email="jamjam@umich.edu",
    description=("Some simple utilites to help automate tasks in Slate."),
    license="BSD",
    packages=find_packages(),
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[],
    install_requires=[
        "beautifulsoup4",
        "loguru",
        "lxml",
        "requests",
        "selenium",
        "umdriver",
    ],
)
