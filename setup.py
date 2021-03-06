#!/usr/bin/env python3
from setuptools import find_packages, setup

from time_logger import (
    __version__ as version,
    __description__ as description,
    __name__ as application,
    __url__ as url,
    __author__ as author,
    __author_email__ as author_email,
    __project_name__ as project_name,
    __cli_handler__ as cli_handler,
)

setup(
    name=application,
    version=".".join([str(part) for part in version]),
    packages=find_packages(),
    url=url,
    license="",
    author=author,
    author_email=author_email,
    description=description,
    install_requires=[
        "click==7.1.2",
        "typer==0.3.2",
    ],
    entry_points={
        "console_scripts": [f"{project_name}={cli_handler}"],
    },
)
