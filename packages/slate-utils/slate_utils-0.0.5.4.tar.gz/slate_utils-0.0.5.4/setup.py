from setuptools import find_packages, setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="slate_utils",
    version="0.0.5.4",
    author="Jamie Davis",
    author_email="jamjam@umich.edu",
    description=("Some simple utilites to help automate tasks in Slate."),
    license="BSD",
    packages=["slate_utils"],
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[],
    install_requires=["loguru", "lxml", "requests", "selenium", "umdriver"],
)
