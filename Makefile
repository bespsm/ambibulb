# MIT License
# Copyright (c) 2021 Sergey B <dkc.sergey.88@hotmail.com>

.PHONY: all build install uninstall purge clean configure
SHELL=/bin/bash

PYTHON=/usr/bin/python3

SYSTEMD_UNIT_FILE=ambibulb.service
SYSTEMD_LOCAL_DIR=./systemd
SYSTEMD_DIR=~/.config/systemd/user

LIRC_LOCAL_FILE=osram-rgb-led.conf
LIRC_LOCAL_DIR=./lirc_conf
LIRC_DIR=/etc/lirc/lircd.conf.d/

all:
	@echo "make build"
	@echo "    Build ambibulb wheel package."
	@echo "make install"
	@echo "    Build, install ambibulb and its dependencies."
	@echo "make configure"
	@echo "    Configure installed ambibulb, lirc and systemd service."
	@echo "make uninstall"
	@echo "    Uninstall ambibulb service."
	@echo "make purge"
	@echo "    Uninstall ambibulb service and its dependencies."
	@echo "make clean"
	@echo "    Remove python artifacts."

build:
	@echo "building ambubulb wheel package..."
	pip3 install --user wheel
	${PYTHON} setup.py sdist bdist_wheel

install: build
	@echo "install ambubulb package..."
	pip3 install --user dist/ambibulb-*.whl

configure:
	@echo "configure ambibulb..."
	ambibulb-config
	@echo "configure ambibulb systemd service..."
	mkdir -p ${SYSTEMD_DIR}
	cp ${SYSTEMD_LOCAL_DIR}/${SYSTEMD_UNIT_FILE} ${SYSTEMD_DIR}
	sed -i '/\b[Service]\b/a Environment=PYTHONUNBUFFERED=1 PATH='$(PATH) ${SYSTEMD_DIR}/${SYSTEMD_UNIT_FILE}
	systemctl --user daemon-reload
	@echo "configure lirc..."
	sudo cp ${LIRC_LOCAL_DIR}/${LIRC_LOCAL_FILE} ${LIRC_DIR}
	sudo systemctl restart lircd
	@echo ""
	@echo "Commands to run:"
	@echo "systemctl --user start ambibulb.service"
	@echo "    Start ambibulb service."
	@echo "systemctl --user stop ambibulb.service"
	@echo "    Stop ambibulb service."
	@echo "systemctl --user status ambibulb.service"
	@echo "    Check ambibulb service status."
	@echo "ambibulb-config"
	@echo "    Configure ambibulb service."

uninstall:
	@echo "uninstall ambibulb package..."
	pip3 uninstall -y ambibulb
	@echo "remove ambibulb systemd service..."
	rm ${SYSTEMD_DIR}/${SYSTEMD_UNIT_FILE}
	systemctl --user daemon-reload
	@echo "remove lirc configuration..."
	sudo rm ${LIRC_DIR}/${LIRC_LOCAL_FILE}
	sudo systemctl restart lircd

purge: uninstall
	@echo "uninstall ambibulb's dependencies..."
	pip3 uninstall -y -r requirements.txt

clean:
	@echo "remove python artifacts..."
	rm -rf *.eggs *.egg-info dist build .cache
