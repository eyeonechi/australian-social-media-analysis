#!/bin/bash

# Docker CE
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce
sudo docker run hello-world

# Docker Compose
sudo curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

# Spark
docker build spark-2 --tag spark-2:2.1.0
git clone https://github.com/AURIN/comp90024.git
cd comp90024/spark
sudo docker build spark-2 --tag spark-2:2.1.0
sudo docker-compose up
export mastercont=`sudo docker ps | grep spark-master | cut -f1 -d' '`

# pyspark
# execfile('/root/wc.py')
# exit()
# exit

sudo docker exec -ti ${mastercont} /bin/bash
sudo docker-compose stop
sudo docker-compose start
