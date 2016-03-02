#-------------------------------------------------------------------------------
# rbt: test_rbt.py
#
# Tests for rbt.py.
#-------------------------------------------------------------------------------
# The MIT License (MIT)
# Copyright (c) 2016 Brian Minard
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#-------------------------------------------------------------------------------
from click.testing import CliRunner
import pytest
import rbt


def test_canonify_url_fixup(review_board_fqdn):
    """ Ensure that URLs are fixed up when they need to be.
    """
    assert 'https://' + review_board_fqdn == rbt.canonify_url(review_board_fqdn)


def test_canonify_url_no_fixup(review_board_url):
    """ Ensure that URLs are not fixed up when they don't need to be.
    """
    assert review_board_url == rbt.canonify_url(review_board_url)


def test_rbt_with_url_only(review_board_fqdn):
    """ Run rbt by specifing only a URL.
    """
    runner = CliRunner()
    result = runner.invoke(rbt.rbt, [ review_board_fqdn ])
    assert 0 < len(result.output)
    assert 0 != result.exit_code


def test_rbt_with_root(review_board_fqdn):
    """ Run rbt by specifing root and a URL.
    """
    runner = CliRunner()
    result = runner.invoke(rbt.rbt, [ 'root', review_board_fqdn ])
    assert 0 < len(result.output)
    assert 0 == result.exit_code


def test_rbt_with_root(review_board_fqdn):
    """ Run rbt by specifing root and a URL.
    """
    runner = CliRunner()
    result = runner.invoke(rbt.rbt, [ review_board_fqdn, 'root' ])
    assert 0 < len(result.output)
    assert 0 != result.exit_code
