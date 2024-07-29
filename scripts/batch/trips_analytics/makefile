.PHONY: help mypy isort, lint-check, lint, neat, test, prepare-environment

# Will include both `.env` if it exists (-)
-include .env
export

SHELL := /bin/bash

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


prepare-venvironment:
	
	@echo "Installing the project's dependencies..."
	(rm -rf venv \
	&& python3 -m virtualenv venv \
	&& source venv/bin/activate \
	&& python3 -m pip install -r requirements/requirements-dev.txt \
	&& python3 -m pip install -r requirements/requirements-test.txt)
	@echo "The Project's environment is ready!!"

#make build_image IMAGE_NAME=seoerick/trip_raw IMAGE_TAG=0.0.1 
build_image:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .