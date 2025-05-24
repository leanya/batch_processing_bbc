#!/bin/bash
set -ex
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo chmod 666 /var/run/docker.sock
sudo usermod -a -G docker ec2-user
sudo yum install git -y
sudo curl -L https://github.com/docker/compose/releases/download/v2.32.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose