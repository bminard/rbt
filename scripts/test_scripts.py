#-------------------------------------------------------------------------------
# rbt: test_rbt.py
#
# Tests for rbt script.
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
import json
import pytest
import subprocess


scripts = [ './rbt', './rbt.py' ]
subcommands = [ 'root', 'review-requests' ]


def check_call(*args):
    """Verify script return code.

    Args:
        args: rbt command-line arguments

    Returns:
        RBT return code.

    Raises:
        CalledProcessError: whenever the subprocess cannot be properly envoked.
    """
    try:
        return subprocess.check_call(list(args))
    except subprocess.CalledProcessError as e:
        return e.returncode


def check_output(*args):
    """Verify script text output.

    Args:
        args: rbt command-line arguments

    Returns:
        RBT return code.

    Raises:
        CalledProcessError: whenever the subprocess cannot be properly envoked.
    """
    try:
        return subprocess.check_output(list(args))
    except subprocess.CalledProcessError as e:
        return e.returncode


@pytest.mark.parametrize("script", scripts)
@pytest.mark.parametrize("subcommand", subcommands)
def test_script_subcommand_no_options(script, subcommand, server):
    """Basic validation of script without any command-line options."""
    assert 0 == check_call(script, subcommand, server.url), "expected zero return code"


@pytest.mark.parametrize("script", scripts)
@pytest.mark.parametrize("subcommand", subcommands)
def test_script_subcommand_with_options(script, subcommand, server):
    """Basic validation of script with unsupported command-line option."""
    assert 0 != check_call(script, subcommand, server.url, '--foo=bar'), "expected non-zero return code"


review_request_parameters = [
        '--counts-only',
        '--time-added-from=2016-03-19',
        '--time-added-to=2016-03-20',
]


@pytest.mark.parametrize("script", scripts)
@pytest.mark.parametrize("parameter", review_request_parameters)
def test_review_requests_with_count_one_option(script, parameter, server):
    """Basic validation of script with one command-line option."""
    assert 0 == check_call(script, 'review-requests', server.url, parameter), "expected zero return code"
    output = json.loads(check_output(script, 'review-requests', server.url, parameter))
    assert 'ok' == output['stat']


@pytest.mark.parametrize("script", scripts)
@pytest.mark.parametrize("p1", review_request_parameters)
@pytest.mark.parametrize("p2", review_request_parameters)
def test_review_requests_with_count_only_option(script, p1, p2, server):
    """Basic validation of script with multiple command-line options."""
    assert 0 == check_call(script, 'review-requests', server.url, p1, p2), "expected zero return code"
    output = json.loads(check_output(script, 'review-requests', server.url, p1, p2))
    assert 'ok' == output['stat']


post_parameters = [
    './test_text_file',
]


@pytest.mark.parametrize("script", scripts)
@pytest.mark.parametrize("parameter", post_parameters)
def test_post_with_file_upload(credentials, script, server, parameter):
    """Validate the post subcommand."""
    if False == server.can_authenticate():
        pytest.skip("cannot authenticate to server: {}".format(server.fqdn))
    assert 0 == check_call(script, 'post', '--username=' +
            credentials['username'], '--password=' + credentials['password'], server.url, parameter), "expected zero return code"
    output =  check_output(script, 'post', '--username=' + credentials['username'],
            '--password=' + credentials['password'], server.url, parameter)
