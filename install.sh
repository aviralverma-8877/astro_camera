#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

python -m ensurepip --upgrade
sudo apt install git -y
cd ~
sudo git clone https://github.com/aviralverma-8877/astro_camera.git

wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.71.tar.gz
tar zxvf bcm2835-1.71.tar.gz
cd bcm2835-1.71/
sudo ./configure && sudo make && sudo make check && sudo make install

cd ..
git clone https://github.com/WiringPi/WiringPi
cd WiringPi
./build

sudo apt-get update -y
sudo apt-get install python3-pip -y
sudo apt-get install python3-pil -y
sudo apt-get install python3-numpy -y
sudo pip3 install RPi.GPIO
sudo pip3 install spidev

sudo pip3 install picamera
sudo pip install numpy
sudo pip install opencv-python

cd ~/astro_camera
sudo ln -sf ~/astro_camera/astro_cam.service /etc/systemd/system/astro_cam.service
sudo systemctl daemon-reload
sudo systemctl start astro_cam.service
sudo systemctl enable astro_cam.service
