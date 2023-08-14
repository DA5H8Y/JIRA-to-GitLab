#! /usr/bin/bash

python ./create_from_file.py

python ./git_auto_pusher.py -d ./Sample -u gitlab.localhost.com
