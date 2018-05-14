#!/bin/bash
# Convenient sonic-track-install.sh script written by Claude Pageau 1-Jul-2016
ver="0.96"
DEST_DIR='sonic-track'  # Default folder install location

cd ~
if [ -d "$DEST_DIR" ] ; then
  STATUS="Upgrade"
  echo "Upgrade sonic-track files"
else  
  echo "New sonic-track Install"
  STATUS="New Install"
  mkdir -p $DEST_DIR
  echo "$DEST_DIR Folder Created"
fi 

cd $DEST_DIR
INSTALL_PATH=$( pwd )

# Remember where this script was launched from
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "-------------------------------------------------------------"
echo "      sonic-track setup.sh script ver $ver"
echo "Install or Upgrade sonic-track motion activated notes"
echo "-------------------------------------------------------------"
echo "1 - Downloading sonic-track github repo files"
echo ""
if [ -e config.py ]; then
  if [ ! -e config.py.orig ]; then
     echo "Save config.py to config.py.orig"
     cp config.py config.py.orig
  fi
  echo "Backup config.py to config.py.prev"
  cp config.py config.py.prev
else
  wget -O config.py -q --show-progress https://raw.github.com/pageauc/sonic-track/master/config.py     
fi

wget -O config-new.py -q --show-progress https://raw.github.com/pageauc/sonic-track/master/config.py
if [ $? -ne 0 ] ;  then
  wget -O config.py https://raw.github.com/pageauc/sonic-track/master/config.py
  wget -O config.py.default https://raw.github.com/pageauc/sonic-track/master/config.py.default
  wget -O config.py.drums https://raw.github.com/pageauc/sonic-track/master/config.py.drums
  wget -O config.py.notes https://raw.github.com/pageauc/sonic-track/master/config.py.notes
  wget -O config.py.notes-drums https://raw.github.com/pageauc/sonic-track/master/config.py.notes-drums
  wget -O sonic-track.sh https://raw.github.com/pageauc/sonic-track/master/sonic-track.sh  
  wget -O sonic-track.py https://raw.github.com/pageauc/sonic-track/master/sonic-track.py
#  wget -O setup.sh https://raw.github.com/pageauc/sonic-track/master/setup.sh 
  wget -O cv32-setup.sh https://raw.github.com/pageauc/opencv3-setup/master/cv32-setup.sh  
  wget -O Readme.md https://raw.github.com/pageauc/sonic-track/master/Readme.md
  # wget -O psonic.py https://raw.github.com/gkvoelkl/python-sonic/master/psonic.py
else
  wget -O config.py -q --show-progress https://raw.github.com/pageauc/sonic-track/master/config.py
  wget -O config.py.default -q --show-progress https://raw.github.com/pageauc/sonic-track/master/config.py.default
  wget -O config.py.drums -q --show-progress https://raw.github.com/pageauc/sonic-track/master/config.py.drums
  wget -O config.py.notes -q --show-progress https://raw.github.com/pageauc/sonic-track/master/config.py.notes
  wget -O config.py.notes-drums -q --show-progress https://raw.github.com/pageauc/sonic-track/master/config.py.notes-drums
  wget -O sonic-track.sh -q --show-progress https://raw.github.com/pageauc/sonic-track/master/sonic-track.sh
  wget -O sonic-track.py -q --show-progress https://raw.github.com/pageauc/sonic-track/master/sonic-track.py
#  wget -O setup.sh -q --show-progress https://raw.github.com/pageauc/sonic-track/master/setup.sh 
  wget -O cv32-setup.sh -q --show-progress https://raw.github.com/pageauc/opencv3-setup/master/cv32-setup.sh  
  wget -O Readme.md -q --show-progress https://raw.github.com/pageauc/sonic-track/master/Readme.md
  # wget -O psonic.py -q --show-progress https://raw.github.com/gkvoelkl/python-sonic/master/psonic.py
fi
  
echo "Done Download"
echo "-------------------------------------------------------------"
echo "2 - Make Required Files Executable"
echo ""
chmod +x *py
chmod -x config*py
# chmod -x psonic*py
chmod +x *sh
echo "Done Permissions"
echo "-------------------------------------------------------------"
# check if system was updated today
NOW="$( date +%d-%m-%y )"
LAST="$( date -r /var/lib/dpkg/info +%d-%m-%y )"
if [ "$NOW" == "$LAST" ] ; then
  echo "4 Raspbian System is Up To Date"
  echo ""  
else
  echo "3 - Performing Raspbian System Update"
  echo "    This Will Take Some Time ...."
  echo ""
  sudo apt-get -y update
  echo "Done Update"
  echo "-------------------------------------------------------------"
  echo "4 - Performing Raspbian System Upgrade"
  echo "    This Will Take Some Time ...."
  echo ""
  sudo apt-get -y upgrade
  echo "Done Upgrade"
fi  
echo "------------------------------------------------"
echo ""  
echo "5 - Installing sonic-track Dependencies"
echo ""
sudo apt-get install -yq python-picamera
sudo apt-get install -yq python3-picamera
sudo apt-get install -yq python-pip
sudo apt-get install -yq git
sudo apt-get install -yq dos2unix
sudo pip install python-osc
git clone https://github.com/gkvoelkl/python-sonic
cd python-sonic
sudo python3 setup.py install
cd ..
rm -r python-sonic

cd $DIR
# Check if install.sh was launched from sonic-track folder
if [ "$DIR" != "$INSTALL_PATH" ]; then
  if [ -e 'setup.sh' ]; then
    echo "$STATUS Cleanup setup.sh"
    rm setup.sh
  fi
fi

echo "Done Dependencies"

echo "Make sure you have
1 opencv3 installed see https://github.com/pageauc/opencv3-setup
2 speaker connected or RPI on HDTV via HTMI cable
3 picamera or webcam installed and working
4 config.py edited as required eg webcam setting if needed
5 For Details See https://github.com/pageauc/sonic-track

To launch
    cd ~/sonic-track
    ./sonic-track.sh

"
echo $DEST_DIR "Good Luck Claude ..."
echo "Bye"

