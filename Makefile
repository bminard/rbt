all: check


check:
	make -C rbtlib check
	make -C scripts check


clean:
	make -C rbtlib clean
	make -C scripts clean
	-/bin/rm -fr venv rbtlib.egg-info timestamp build dist .cache


.PHONY: install
install: virtual-environment
	make -C rbtlib install
	make -C scripts install

.PHONY: virtual-environment
virtual-environment: timestamp
timestamp: venv
	touch $@
venv: virtualenv.sh requirements.txt
	sh virtualenv.sh test
	@echo ""
	@echo "****************************************************************************"
	@echo "* Run . venv/bin/activate to activate the virtual development environment! *"
	@echo "****************************************************************************"
	@echo ""


.PHONY: uninstall
uninstall: clean
	make -C rbtlib uninstall
	make -C scripts uninstall
