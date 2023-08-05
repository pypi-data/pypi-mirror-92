# -*- coding: utf-8 -*-
"""setup.py."""
from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    "fastapi>=0.61.1",
    "Jinja2>=2.11.2",
    "uvicorn>=0.12.2",
    "aiofiles>=0.5.0"
]
VERSION = '0.1.2'

setup(
    name='xtapi',
    version=VERSION,
    description='Web api',
    author='codingcat',
    author_email='istommao@gmail.com',
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    package_dir={'xtapi': 'xtapi'},
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/istommao/xtapi',
    keywords='xtapi is a web api base on FastAPI',
    entry_points="""
    [console_scripts]
    xtapi=xtapi.script:main
    """
)
