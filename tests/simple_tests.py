#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nose
import os

import memtop


# Tests
def graph_format_test():
    memtop.graph_format(1, 2, True)
    memtop.graph_format(1, 2, False)
    for i in range(0, 60000000, 10000):
        memtop.graph_format(0, i, False)
        memtop.graph_format(i, 0, False)


def parser_test():
    memtop.get_parser()


def format_mem_numb_test():
    nose.tools.assert_equal(memtop.format_mem_numb(12), "12 B")
    nose.tools.assert_equal(
        memtop.format_mem_numb(1023), "1023 B"
    )  # TODO: should be kiB
    nose.tools.assert_equal(memtop.format_mem_numb(1200), "1.2 kB")
    nose.tools.assert_equal(
        memtop.format_mem_numb(1200000), "1.1 MB"
    )  # TODO: Is this right?


def get_private_mem_test():
    memtop.get_private_mem(os.getpid())


def get_cur_mem_use_test():
    memtop.get_cur_mem_use()


def check_swapping_test():
    memtop.check_swapping(True, True)
    memtop.check_swapping(True, False)
    # memtop.check_swapping(False, True)
    # memtop.check_swapping(False, False)


def check_py_version_test():
    memtop.check_py_version()
