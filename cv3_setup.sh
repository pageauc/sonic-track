#!/bin/bash
# Script to assist with installing Camerafeed and OpenCV3
# If problems are encountered exit to command to try to resolve
# Then retry menu pick again or continue to next step

function do_anykey ()
{
   echo "------------------------------"
   echo "  Review messages for Errors"
   echo "  Exit to Console to Resolve"
   echo "------------------------------"   
   read -p "M)enu E)xit ?" choice
   case "$choice" in
      m|M ) echo "Back to Main Menu"
       ;;
      e|E ) echo "Install Aborted. Bye"
            exit 1
       ;;
        * ) echo "invalid Selection"
            exit 1 ;;
   esac
}

function do_rpi_update ()
{
   cd ~/   
   # Update Raspian to Lastest Releases
   echo "Updating Raspbian Please Wait ..."
   echo "---------------------------------"    
   sudo apt-get update
   echo "Upgrading Rasbian Please Wait ..."
   echo "---------------------------------"    
   sudo apt-get upgrade
   # Perform rpi-update
   echo "updating Raspbian rpi-update"
   echo "----------------------------"    
   sudo rpi-update
   echo "----------------------------"    
   echo "It is Time to Reboot after"
   echo "updating Raspbian Jessie"
   echo "----------------------------"    
   read -p "Reboot Now? (y/n)?" choice
   case "$choice" in 
     y|Y ) echo "yes"
           echo "Rebooting Now"
           sudo reboot
           ;;
     n|N ) echo "Back To Main Menu"
           ;;
       * ) echo "invalid Selection"
           exit 1
           ;;
  esac
}

function do_camerafeed_clone ()
{
   cd ~/  
   # Clone Camerafeed Repo
   echo "Cloning Camerafeed from Github"
   echo "------------------------------"     
   echo "Please wait ...."
   git clone https://github.com/liquidg3/Camerafeed
   # Copy class libraries to local lib
   echo "copy ~/Camerafeed/camerafeed/ /usr/local/lib/python2.7/dist-packages"
   echo "--------------------------------------------------------------------"     
   sudo cp -r ~/Camerafeed/camerafeed/ /usr/local/lib/python2.7/dist-packages
   echo "copy ~/Camerafeed/camerafeed/ /usr/local/lib/python3.4/dist-packages"
   echo "--------------------------------------------------------------------"      
   sudo cp -r ~/Camerafeed/camerafeed/ /usr/local/lib/python3.4/dist-packages
   do_anykey
}

function do_camerafeed_dep ()
{
   cd ~/
   # Install program Dependencies
   echo "Camerafeed - Installing Dependencies"
   echo "------------------------------------"       
   echo "This will take a while Please Wait"
   sudo apt-get install -y libevent-dev
   sudo apt-get install -y python-picamera
   sudo apt-get install -y python-configparser
   sudo apt-get install -y python-gevent
   sudo apt-get install -y python-requests
   sudo apt-get install -y python-shapely
   sudo pip3 install shapely
   sudo pip install grequests 
   sudo pip3 install grequests      
   sudo pip install imutils
   sudo pip3 install imutils
   do_anykey
}

function do_cv3_dep ()
{
   cd ~/
   # Install opencv3 build dependencies
   echo "Installing opencv3 build and run dependencies"
   echo "---------------------------------------------"       
   sudo apt-get install -y build-essential git cmake pkg-config
   sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
   sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
   sudo apt-get install -y libxvidcore-dev libx264-dev
   sudo apt-get install -y libgtk2.0-dev
   sudo apt-get install -y libatlas-base-dev gfortran
   sudo apt-get install -y python2.7-dev python3-dev     
   wget https://bootstrap.pypa.io/get-pip.py
   sudo python get-pip.py
   sudo pip install numpy
   do_any_key   
}

function do_cv3_get ()
{
   cd ~/
   echo "Download and unzip opencv 3.0.0"
   echo "-------------------------------"    
   # Install opencv3 download and unzip
   wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.0.0.zip 
   unzip opencv.zip 
   do_anykey
}

function do_cv3_install ()
{
   cd ~/
   echo "cmake prior to compiling opencv 3.0.0"
   echo "-----------------------------------"       
   # Compile opencv3 for RPI
   cd ~/opencv-3.0.0/
   mkdir build
   cd build
   cmake -D CMAKE_BUILD_TYPE=RELEASE \
         -D CMAKE_INSTALL_PREFIX=/usr/local \
         -D INSTALL_C_EXAMPLES=OFF \
         -D INSTALL_PYTHON_EXAMPLES=ON \
         -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.0.0/modules \
         -D BUILD_EXAMPLES=ON ..
      echo "--------------------------------" 
      echo " Check if cmake above had errors"
      echo "--------------------------------" 
      echo "n exits to console"
      read -p "Was cmake successful y/n ?" choice
      case "$choice" in
        y|Y ) echo "Compiling openCV3 ver 3.0.0"
              echo "This will take approx 1h 40 min"      
              make -j4
              echo "------------------------------------"  
              echo " Check if opencv compile had errors "
              echo "------------------------------------"               
              read -p "Was Compile Successful y/n ?" choice
              case "$choice" in            
                y|Y ) echo "Installing opencv 3.0.0"
                      sudo make install
                      ;;
                n|N ) echo "Please Investigate Problem and Try Again"
                      exit 1
                      ;;
                  * ) echo "invalid Selection"
                      exit 1
                      ;;  
              esac                      
            ;;
        n|N ) echo "cmake failed so Investigate Problem and Try again"
              exit 1
              ;;
          * ) echo "invalid Selection"
              exit 1
              ;;
      esac
}


#------------------------------------------------------------------------------
function do_about()
{
  whiptail --title "About" --msgbox " \
   Camerafeed project Install Assist
      written by Claude Pageau

This Menu will help install Feedcamera github
project, dependencies and Optionally Opencv 3
Note Feedcamera Libraries will be installed
to /usr/local/lib/python3.4/dist-packages
and /usr/local/lib/python2.7/dist-packages

You can run Camerafeed from a Desktop Terminal
or SSH console (cannot view video feed)
to view opencv window per settings.ini
This will take input from pi camera or
a video file depending on settings.ini
for Live Camera set
pi : True
show_window : True

To Run from desktop terminal or console
depending on how you have things configured
Run

cd ~/Camerafeed
python3 run.py                    

             Good Luck 
\
" 35 70 35
}


#------------------------------------------------------------------------------
function do_main_menu ()
{
  SELECTION=$(whiptail --title "Camerafeed Install" --menu "Arrow/Enter Selects or Tab Key" 20 70 10 --cancel-button Quit --ok-button Select \
  "a " "Raspbian Jessie Update, Upgrade and rpi-update" \
  "b " "Camerafeed Clone from GitHub and Install libs" \
  "c " "Camerafeed Install Dependencies" \
  "d " "OpenCV3 Download and Unzip" \
  "e " "OpenCV3 Install Build Dependencies " \
  "f " "OpenCV3 Make, Compile and Install" \
  "g " "Camerafeed Edit settings.ini" \
  "h " "About" \
  "q " "Quit Menu Back to Console"  3>&1 1>&2 2>&3)

  RET=$?
  if [ $RET -eq 1 ]; then
    exit 0
  elif [ $RET -eq 0 ]; then
    case "$SELECTION" in
      a\ *) do_rpi_update ;;
      b\ *) do_clone_camerafeed ;;
      c\ *) do_camerafeed_dep ;;
      d\ *) do_cv3_get;;
      e\ *) do_cv3_dep ;;
      f\ *) do_cv3_install ;; 
      g\ *) nano ~/Feedcamera/settings.ini ;;
      h\ *) do_about ;;
      q\ *) clear
            exit 0 ;;
         *) whiptail --msgbox "Programmer error: unrecognized option" 20 60 1 ;;
    esac || whiptail --msgbox "There was an error running selection $SELECTION" 20 60 1
  fi
}

while true; do
   do_main_menu
done

echo "Try running Camerafeed App"
echo "Edit the ~/Camerafeed/settings.ini and set pi=True for pi-camera module"
echo "Run Pi desktop and open terminal session then"
echo "cd ~/Camerafeed"
echo "python3 run.py"
echo " You should see a 320x200 video feed from the camera"
echo "Good Luck ..."

