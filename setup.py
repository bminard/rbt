#-------------------------------------------------------------------------------
# rbtlib: setup.py
#
# Rbt setup script.
#
# Credit to Eli Bendersky's pss/setup.py.
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
import os, sys
from rbtlib import __version__


try:
    from setuptools import setup
    use_setuptools = True
except ImportError:
    from distutils.core import setup
    use_setuptools = False


if use_setuptools:
    # Setuptools provides an "entry points" facility to automatically generate
    # scripts that work in the same way as the supplied "rbt" script. This
    # feature is more portable to other platforms than providing a manually
    # created script, so we use that feature if it is available.
    # By using entry points, we get a "rbt" shell script on Unix, and a
    # "rbt.exe" command on Windows, without any extra effort.
    extra_args = {
        'entry_points': {
            'console_scripts': 'rbt = rbtlib.rbt:rbt',
         },
    }
else:
    # Setuptools is not available, so fall back to custom built scripts.
    extra_args = {
        'scripts': ['scripts/rbt.py', 'scripts/rbt'],
    }


try:
    with open('README.rst', 'rt') as readme:
        description = '\n' + readme.read()
except IOError:
    # maybe running setup.py from some other dir
    description = ''


setup(
    author = "Brian Minard",
    author_email = "bminard@flatfoot.ca",
    license = "MIT",
    description = 'A Client-Side library for Review Board.',
    long_description = description,
    maintainer = 'Brian Minard',
    url = 'https://github.com/bminard/rbtlib',
    name = 'rbtlib',
    version = __version__,
    packages = [
        'rbtlib',
    ],
    install_requires = [
        'Click',
        'python-magic',
        'requests',
    ],
    extras_require = {
        'docs': [
            'Sphinx',
        ],
        'test': [
            'pytest',
            'radon',
            'xenon',
        ],
    },
    platforms = 'Cross Platform',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
    ],

    **extra_args
)
