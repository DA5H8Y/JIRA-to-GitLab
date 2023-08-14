#! /usr/bin/bash
./install-docker.sh

python -m venv env
source env/bin/activate

python -m pip install -r requirements.txt
