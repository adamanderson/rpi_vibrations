# check if sudo is used
if [ "$(id -u)" != 0 ]; then
  echo 'Sorry, you need to run this script with sudo'
  exit 1
fi

apt-get install -y smbus i2c-tools              # I2C
apt-get install -y python-dev python-rpi        # GPIO python control
apt-get install -y git                          # git
apt-get install -y avahi-daemon                 # mDNS
apt-get install -y emacs                        # in case of desperation

touch /boot/ssh                                 # enable ssh https://www.raspberrypi.org/documentation/remote-access/ssh/

