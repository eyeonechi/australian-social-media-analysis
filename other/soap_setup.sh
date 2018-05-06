#!/bin/bash

sudo apt install nodejs-legacy
sudo apt install npm
cd comp90024/soapsample
sudo npm install

# Server
node serverEcho

# Client
node clientEcho
node clientWeather
