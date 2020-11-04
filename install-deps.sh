#!/bin/bash

sudo apt update
sudo apt install -y libhdf5-dev
sudo apt install -y libatlas-base-dev

wget https://github.com/Qengineering/Tensorflow-Raspberry-Pi/raw/master/tensorflow-2.1.0-cp37-cp37m-linux_armv7l.whl
pip3 install pip --upgrade
pip3 install tensorflow-2.1.0-cp37-cp37m-linux_armv7l.whl
pip3 install h5py==2.10.0
pip3 install soundfile pyaudio

cd raspberrypi3-yamnet-sed/yamnet
wget https://storage.googleapis.com/audioset/yamnet.h5
cp .asoundrc ..

cd
git clone https://github.com/google/aiyprojects-raspbian
cd aiyprojects-raspbian
git checkout master
sudo scripts/configure-driver.sh
sudo scripts/install-alsa-config.sh