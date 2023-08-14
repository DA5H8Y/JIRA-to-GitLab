#! /usr/bin/bash

#Clean-up old installs
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; 
    do sudo apt-get remove $pkg;
done

rm -r $HOME/.docker/desktop
sudo rm /usr/local/bin/com.docker.cli
sudo apt purge docker-desktop
sudo rm ~/.config/systemd/user/docker-desktop.service
sudo rm ~/.local/share/systemd/user/docker-desktop.service

# Add Docker Repository
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install prerequisites
sudo apt-get update
sudo apt install gnome-terminal

# Install latest docker engine
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify the install
sudo docker run hello-world
docker compose version