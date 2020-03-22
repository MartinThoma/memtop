#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Core Library modules
import os

# First party modules
import memtop


# Tests
def test_graph_format():
    memtop.graph_format(1, 2, True)
    memtop.graph_format(1, 2, False)
    for i in range(0, 60000000, 10000):
        memtop.graph_format(0, i, False)
        memtop.graph_format(i, 0, False)


def test_parser():
    memtop.get_parser()


def test_format_mem_numb():
    assert memtop.format_mem_numb(12) == "12 B"
    assert memtop.format_mem_numb(1023) == "1023 B"  # TODO: should be kiB
    assert memtop.format_mem_numb(1200) == "1.2 kB"
    assert memtop.format_mem_numb(1200000) == "1.1 MB"  # TODO: Is this right?


def test_get_private_mem():
    memtop.get_private_mem(os.getpid())


def test_get_cur_mem_use():
    memtop.get_cur_mem_use()


def test_check_swapping():
    memtop.check_swapping(True, True)
    memtop.check_swapping(True, False)
    # memtop.check_swapping(False, True)
    # memtop.check_swapping(False, False)


def test_check_py_version():
    memtop.check_py_version()
