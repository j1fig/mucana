mucana
======

Website and configuration for mucana.org.


## Requirements

In order to deploy the infrastructure for mucana.org you will need

1. terraform 0.12+
2. Python 3.6+

After getting these you should create the python virtualenv and install the requirements via

	python3 -m venv .venv
	. ./venv/bin/activate  # the rest of this document will assum you have this venv active.
	pip install -r requirements.txt


## Usage

To fully deploy

	./deploy --init  # make coffee
	terraform apply  # drink coffee
	./deploy --sync
