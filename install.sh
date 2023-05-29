#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

sudo apt update
sudo apt install python3-pip -y
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

sudo apt install python3-opencv -y
sudo pip3 install picamera
sudo pip install numpy

sudo cat "dtoverlay=dwc2" >> /boot/config.txt
sudo cat "dwc2" >> /etc/modules

sudo dd bs=1M if=/dev/zero of=/piusb.bin count=2048
sudo mkdosfs /piusb.bin -F 32 -I
sudo mkdir /mnt/usb_share
sudo cat "/piusb.bin /mnt/usb_share vfat users,umask=000 0 2" >> /etc/fstab
sudo mount -a

cd ~/astro_camera
sudo chmod +x main
sudo ln -sf ~/astro_camera/astro_cam.service /etc/systemd/system/astro_cam.service
sudo systemctl daemon-reload
sudo systemctl start astro_cam.service
sudo systemctl enable astro_cam.service

sudo reboot