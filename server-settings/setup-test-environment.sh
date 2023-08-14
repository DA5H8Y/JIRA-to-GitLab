#! /usr/bin/bash

echo \
"127.0.0.1 jira.internal \
 127.0.0.1 gitlab.internal" | \
sudo tee /etc/hosts > /dev/null

export GITLAB_HOME='./env'
sudo docker compose up -d