#-------------------------------------------------------------------------------
# rbtlib: test_rbt.py
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
import collections
import pytest
import rbt
import requests


@pytest.fixture
def context(session):
    """Mock-up of the Click context.

    Args:
        session: the HTTP session.

    Returns:
        A mock-up of the Click context.
    """
    args = dict()
    obj = dict()
    obj['session'] = session
    args['obj'] = obj
    ctx = collections.namedtuple('ctx', 'obj') # FIXME: ctx is read-only.
    return ctx(**args)


def test_canonify_scheme_with_fixup(context, server):
    """Ensure that URLs are fixed up when they need to be."""
    assert server.url == rbt.canonify_url(context, server.fqdn)


def test_canonify_scheme_without_fixup(context, server):
    """Ensure that URLs are not fixed up when they don't need to be."""
    assert server.url == rbt.canonify_url(context, server.url)


def test_login_ok(context, server, credentials):
    """Ensure we can login."""
    if(False == server.can_authenticate()):
        pytest.skip("cannot authenticate to server: {}".format(server.fqdn))
    assert 200 ==  rbt.login(context, server.url, credentials['username'], credentials['password'])


def test_login_fail(context, server):
    """Ensure we can't login."""
    assert 200 ==  rbt.login(context, server.url, 'username', 'password')


def test_rbt_with_fqdn_only(context, server):
    """Run rbt by specifing only a fully qualified domain name."""
    runner = CliRunner()
    result = runner.invoke(rbt.rbt, args = [ server.fqdn ])
    assert 0 < len(result.output)
    assert 0 != result.exit_code


# RBT subcommand and arguments.
subcommand_list = [
    [ 'root' ],
    [ 'review-requests' ],
    [ 'post', 'foo' ]
]


@pytest.mark.parametrize("subcommand", subcommand_list)
def test_rbt_with_subcommand_url_correct_position(context, subcommand, server):
    """Run rbt by specifing a subcommand and URL in the correct order."""
    runner = CliRunner()
    result = runner.invoke(rbt.rbt, args = [ subcommand[0], server.fqdn ].extend(subcommand[1:]), obj = dict())
    assert 0 < len(result.output)
    assert 0 == result.exit_code


@pytest.mark.parametrize("subcommand", subcommand_list)
def test_rbt_with_subcommand_url_wrong_position(context, subcommand, server):
    """Run rbt by specifing a subcommand and URL in the wrong order."""
    runner = CliRunner()
    if 1 < len(subcommand):
        args = [ server.fqdn ]
        args.extend(subcommand[0:])
    else:
        args = [ server.fqdn, subcommand ]
    result = runner.invoke(rbt.rbt, args, obj = dict())
    assert result.output == 'Usage: rbt [OPTIONS] COMMAND [ARGS]...\n\nError: No such command "{}".\n'.format(server.fqdn)
    assert 0 != result.exit_code
