#! /bin/bash

# This file will download node js onto the raspberry pi and do all the installing automatically 

# First we want to make sure python3 is installed 

# We then need to install node js and npm 
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install RPi.GPIO
sudo pip3 install spidev
sudo pip3 install qrcode

git clone https://github.com/AlexChapple/python-wifi-connect.git

git config --global credential.helper store
git clone https://github.com/AlexChapple/ChappleFrame.git

wget https://unofficial-builds.nodejs.org/download/release/v18.16.0/node-v18.16.0-linux-armv6l.tar.xz
tar xvfJ node-v18.16.0-linux-armv6l.tar.xz
sudo cp -R node-v18.16.0-linux-armv6l/* /usr/local
rm -rf node-*

cd ChappleFrame/
npm install 

sudo raspi-config
sudo reboot