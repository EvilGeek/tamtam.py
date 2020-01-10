import pathlib
import re

from setuptools import find_packages, setup

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

    return [
        "aiohttp>=3.5.4,<4.0",
        "pydantic>=0.30,<1.0",
        "ujson>=1.35,<2.0",
    ]


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


DEPENDENCIES_INFO = """
DEPENDENCIES-INFO:

===========================================================
Name: ujson
Version: 1.35
Summary: Ultra fast JSON encoder and decoder for Python
Home-page: http://www.esn.me
Author: Jonas Tarnstrom
Author-email: jonas.tarnstrom@esn.me
License: BSD License
===========================================================
Name: aiohttp
Version: 3.5.4
Summary: Async http client/server framework (asyncio)
Home-page: https://github.com/aio-libs/aiohttp
Author: Nikolay Kim
Author-email: fafhrd91@gmail.com
License: Apache 2
===========================================================
Name: yarl
Version: 1.3.0
Summary: Yet another URL library
Home-page: https://github.com/aio-libs/yarl/
Author: Andrew Svetlov
Author-email: andrew.svetlov@gmail.com
License: Apache 2
===========================================================
"""
