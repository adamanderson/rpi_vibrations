# check if sudo is used
if [ "$(id -u)" != 0 ]; then
  echo 'Sorry, you need to run this script with sudo'
fi

apt-get install -y python-smbus python3-smbus i2c-tools       # I2C
apt-get install -y python-dev python-rpi.gpio python3-dev python3-rpi.gpio  # GPIO python control
apt-get install -y git                                        # git
apt-get install -y avahi-daemon                               # mDNS
apt-get install -y emacs ipython python3-ipython              # in case of desperation
apt-get install -y python-numpy python-scipy python-matplotlib
apt-get install -y python3-numpy python3-scipy python3-matplotlib

touch /boot/ssh                                 # enable ssh https://www.raspberrypi.org/documentation/remote-access/ssh/

git clone http://github.com/adamanderson/python_tb6612fng /home/pi/python_tb6612fng
git clone http://github.com/adamanderson/python_mma8451 /home/pi/python_mma8451

chown -R pi:pi /home/pi/python_tb6612fng
chown -R pi:pi /home/pi/python_mma8451
