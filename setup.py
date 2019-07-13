import pathlib
import re

from setuptools import find_packages, setup

try:
    from pip.req import parse_requirements
except ImportError:  # pip >= 10.0.0
    from pip._internal.req import parse_requirements


WORK_DIR = pathlib.Path(__file__).parent

code = (WORK_DIR / "tamtam" / "__init__.py").read_text("utf-8")

try:
    version = re.findall(r"""^__version__ = "([^']+)"\r?$""", code, re.M)[0]
except IndexError:
    raise RuntimeError("Unable to determine version.")


with open("readme.rst", "r", encoding="utf-8") as f:
    description = f.read()


def get_requirements():
    """
    Read requirements from 'requirements txt'
    :return: requirements
    :rtype: list
    """
    file = WORK_DIR / "requirements.txt"

    install_reqs = parse_requirements(str(file), session="hack")
    return [str(ir.req) for ir in install_reqs]


setup(
    name="tamtampy",
    version=version,
    packages=find_packages(exclude=("examples.*", "test.*", "docs", "test", "static")),
    url="https://github.com/uwinx/tamtam.py",
    license="MIT",
    author="Martin Winks",
    requires_python=">=3.7",
    author_email="mpa@snejugal.ru",
    description="Async and convenient comrade mayor's messenger API wrapper",
    long_description=description,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=get_requirements(),
    package_data={"": ["requirements.txt"]},
    include_package_data=False,
    keywords="dev.tamtam.chat api asynchronous wrapper",
)
