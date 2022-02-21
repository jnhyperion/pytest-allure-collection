import os
from setuptools import setup, find_packages

current_dir = os.path.abspath(os.path.dirname(__file__))

requires = ["pytest", "allure-pytest"]

about = {}
with open(os.path.join(current_dir, "pytest_allure_collection", "__version__.py")) as f:
    exec(f.read(), about)

VERSION = about["__version__"]

setup(
    version=VERSION,
    name="pytest-allure-collection",
    packages=find_packages(),
    description=f"pytest plugin to collect allure markers without running any tests",
    author="Johnny Huang",
    author_email="jnhyperion@gmail.com",
    url="https://github.com/jnhyperion/pytest-allure-collection",
    keywords="pytest allure",
    entry_points={"pytest11": ["pytest-allure-collection = pytest_allure_collection"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Framework :: Pytest",
    ],
    python_requires=">=3.8",
    install_requires=requires,
)
