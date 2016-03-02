#-------------------------------------------------------------------------------
# rbt: rbt.py
#
# Entry point for command-line tool.
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
import click
import json
import review_requests as review_requests_resource
import root as root_resource
import sys
from urlparse import urlparse


def canonify_url(url):
    """ Create a canonical URL for consumption by the library.
    """
    url_components = urlparse(url)
    if 0 == len(url_components.scheme):
        url = 'https://' + url
    return url


def beautify(response):
    """ Beautify response.
    """
    return json.dumps(response, sort_keys = True, indent = 2)


def url_argument(f):
    """ Apply the URL argument to each command in the group.
    """
    def callback(ctx, param, url):
        return canonify_url(url)
    return click.argument('url', callback=callback)(f)


@click.group()
def rbt():
    pass


@rbt.command()
@url_argument
def root(url):
    """ Show root resource.
    """
    print beautify(root_resource.get(url))
    sys.exit


@rbt.command(name = 'review-requests')
@click.option('--counts-only', is_flag = True, 
    help='If specified, a single count field is returned with the number of results.')
@click.option('--time-added-from',
    help='The earliest date/time the review request is added.')
@click.option('--time-added-to',
    help='The latest date/time the review request is added.')
@url_argument
def review_requests(url, counts_only, time_added_from, time_added_to):
    """ Show review requests resource.

    The date and time format is YYYY-MM-DD HH:MM:SS or
    {yyyy}-{mm}-{dd}T{HH}:{MM}:{SS} with an optional timezone appended as
    -{HH:MM}.
    """
    query_dict = dict()
    if counts_only:
        query_dict['counts-only'] = True
    if time_added_from:
        query_dict['time-added-from'] = time_added_from
    if time_added_to:
        query_dict['time-added-to'] = time_added_to
    print beautify(review_requests_resource.get(url, query_dict))
    sys.exit
