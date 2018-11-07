# rpi_vibrations
Control software for vibration motor and accelerometer with a raspberry pi

sudo apt-get install git
git clone https://github.com/adamanderson/rpi_vibrations

## Flashing an SD card with Raspbian on Mac OS
```
diskutil list
diskutil unmountDisk /dev/<my disk>
sudo dd bs=1m if=2018-06-27-raspbian-stretch-lite.img of=/dev/<my disk>
```
Use <ctrl-t> to get the status of `dd` while it runs.

## Manage time servers in Raspbian
Raspbian uses `systemd-timesyncd` by default as a lightweight NTP server. NTP is relatively in important on Raspberry Pi because the system lacks a real-time clock (RTC) chip for cost reasons. The configuration file for this service is `/etc/systemd/timesyncd.conf`. To change the NTP server, for example, uncomment and edit the `NTP` line, then restart the service:
```
systemctl restart systemd-timesyncd
```
