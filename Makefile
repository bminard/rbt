#-------------------------------------------------------------------------------
# rbtlib: Makefile
#
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
all: check docs


.PHONY: check
check: metrics
	make -C rbtlib check
	make -C scripts check


.PHONY: clean
clean:
	make -C docs clean
	make -C rbtlib clean
	make -C scripts clean
	-/bin/rm -fr build dist .cache *.pyc


.PHONY: docs
docs:
	make -C docs html

.PHONY: install
install: virtual-environment
	make -C rbtlib install
	make -C scripts install


.PHONY: virtual-environment
virtual-environment: virtualenv.sh requirements.txt
	sh virtualenv.sh docs test


.PHONY: uninstall
uninstall: clean
	make -C rbtlib uninstall
	make -C scripts uninstall
	-/bin/rm -fr rbtlib.egg-info


.PHONY: metrics
metrics:
	radon cc -as .
	xenon --max-absolute C --max-modules A --max-average A .
