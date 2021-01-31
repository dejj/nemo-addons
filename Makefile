usage:
	# Usage:
	#     `make link` to link files to ~/.local/share
	# or  `make install` to copy files to ~/usr/share 
	# then restart nemo

MAKEFILE_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

link:
	mkdir --parents ~/.local/share/nemo/actions
	mkdir --parents ~/.local/share/nemo-python/extensions
	ln --symbolic --force $(MAKEFILE_DIR)/nemo/actions/fopen.py ~/.local/share/nemo/actions
	ln --symbolic --force $(MAKEFILE_DIR)/nemo/actions/mcomix.nemo_action ~/.local/share/nemo/actions
	ln --symbolic --force $(MAKEFILE_DIR)/nemo-python/extensions/tagged-media-column.py ~/.local/share/nemo-python/extensions

install:
	sudo mkdir --parents /usr/share/nemo/actions
	sudo mkdir --parents /usr/share/nemo-python/extensions
	sudo cp --recursive nemo /usr/share
	sudo cp --recursive nemo-python /usr/share
