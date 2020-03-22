# Core Library modules
import io
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(file_name):
    """Read a text file and return the content as a string."""
    with io.open(
        os.path.join(os.path.dirname(__file__), file_name), encoding="utf-8"
    ) as f:
        return f.read()


config = {
    "name": "memtop",
    "version": "1.0.4",
    "author": "Tibor Bamhor, Martin Thoma",
    "author_email": "info@martin-thoma.de",
    "maintainer": "Martin Thoma",
    "maintainer_email": "info@martin-thoma.de",
    "packages": ["memtop"],
    "scripts": ["bin/memtop"],
    "platforms": ["Linux", "MacOS X"],
    "url": "https://github.com/MartinThoma/memtop",
    "license": "GPLv2",
    "description": "view memory consumption of processes",
    "long_description": read("README.md"),
    "long_description_content_type": "text/markdown",
    "install_requires": ["argparse",],
    "keywords": ["memory", "consumption"],
    "download_url": "https://github.com/MartinThoma/memtop",
    "classifiers": [
        "Development Status :: 7 - Inactive",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],
    "zip_safe": False,
    "test_suite": "nose.collector",
}

setup(**config)
