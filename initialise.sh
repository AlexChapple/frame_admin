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

git clone https://github.com/AlexChapple/python-wifi-connect.git

git config --global credential.helper store
git clone https://github.com/AlexChapple/ChappleFrame.git

sudo raspi-config
sudo reboot