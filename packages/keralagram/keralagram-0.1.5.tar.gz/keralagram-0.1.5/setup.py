#!/usr/bin/env python
import re
from setuptools import setup, find_packages
from io import open


def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()


with open("keralagram/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]


setup(
    name="keralagram",
    version=version,
    description='Asynchronous Python API for building Telegram bots',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/KeralaBots/Keralagram",
    author='Anand P S',
    author_email='anandpskerala@gmail.com',

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries'
    ],
    keywords="telegram asyncio bot",
    packages=find_packages(exclude=["tests*"]),
    install_requires=['httpx[http2]>=0.13.3'],
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest', 'testfixtures']
)