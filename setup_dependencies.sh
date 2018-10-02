# check if sudo is used
if [ "$(id -u)" != 0 ]; then
  echo 'Sorry, you need to run this script with sudo'
  exit 1
fi

apt-get install -y smbus i2c-tools
apt-get install -y python-dev python-rpi