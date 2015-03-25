try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'memtop',
    'version': '1.0.2',
    'author': 'Tibor Bamhor, Martin Thoma',
    'author_email': 'info@martin-thoma.de',
    'maintainer': 'Martin Thoma',
    'maintainer_email': 'info@martin-thoma.de',
    'packages': ['memtop'],
    'scripts': ['bin/memtop'],
    'platforms': ['Linux', 'MacOS X'],
    'url': 'https://github.com/MartinThoma/memtop',
    'license': 'GPLv2',
    'description': 'view memory consumption of processes',
    'long_description': ("memtop is command line utility to help user to find "
                         "out what applications uses biggest portions of the "
                         "memory (RAM+swap), sorted in decreasing order. "
                         "It lists private/writeable memory only, that is "
                         "without shared memory. Typical use is when you need "
                         "to reduce the overall RAM consumption or when you "
                         "encounter performance problems. "
                         "Memtop gets data from /proc/ virtual filesystem."),
    'install_requires': [
        "argparse",
    ],
    'keywords': ['memory', 'consumption'],
    'download_url': 'https://github.com/MartinThoma/memtop',
    'classifiers': ['Development Status :: 3 - Alpha',
                    'Environment :: Console',
                    'Intended Audience :: Developers',
                    'License :: OSI Approved :: GNU General Public License (GPL)',
                    'Natural Language :: English',
                    'Programming Language :: Python :: 2.7',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.3',
                    'Programming Language :: Python :: 3.4',
                    'Topic :: Software Development',
                    'Topic :: Utilities'],
    'zip_safe': False,
    'test_suite': 'nose.collector'
}

setup(**config)
