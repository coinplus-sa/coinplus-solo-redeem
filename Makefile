# Makefile

SHELL := /bin/bash

directory = $(shell pwd)

create_virtualenv:
	python3 -m venv ${directory}/virtualenv

build: create_virtualenv 
	source ${directory}/virtualenv/bin/activate && cd src && python setup.py develop
	
clean:
	rm -rf ${directory}/virtualenv

run:
	source ${directory}/virtualenv/bin/activate && coinplus_solo_redeem
