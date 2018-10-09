# rpi_vibrations
Control software for vibration motor and accelerometer with a raspberry pi

sudo apt-get install git
git clone https://github.com/adamanderson/rpi_vibrations

# Flashing an SD card with Raspbian on Mac OS
```
diskutil list
diskutil unmountDisk /dev/<my disk>
sudo dd bs=1m if=2018-06-27-raspbian-stretch-lite.img of=/dev/<my disk>
```
Use <ctrl-t> to get the status of `dd` while it runs.
