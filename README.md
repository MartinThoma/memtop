[![Build Status](https://travis-ci.org/MartinThoma/memtop.svg?branch=master)](https://travis-ci.org/MartinThoma/memtop)
[![Coverage Status](https://img.shields.io/coveralls/MartinThoma/memtop.svg)](https://coveralls.io/r/MartinThoma/memtop?branch=master)
[![Documentation Status](http://img.shields.io/badge/docs-latest-brightgreen.svg)](http://pythonhosted.org/memtop)
[![Code Health](https://landscape.io/github/MartinThoma/memtop/master/landscape.svg)](https://landscape.io/github/MartinThoma/memtop/master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# memtop
memtop is command line utility to help user to find out what applications uses
biggest portions of the memory (RAM+swap), sorted in decreasing order. It lists
private/writeable memory only, that is without shared memory. Typical use is
when you need to reduce the overall RAM consumption or when you encounter
performance problems.

Memtop gets data from `/proc/` virtual filesystem.
