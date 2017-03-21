# Raspberry Pi Sonic Track Demo
### Track x,y moving object positions and generate sounds via sonic-pi.  
### Uses pi-camera, python3, Opencv3, python-sonic, pythonosc and sonic-pi 

### Quick Install   
Easy Install of sonic-track onto a Raspberry Pi Computer with latest Raspbian.
This is a whiptail menu system that allows install of opencv3 if required 

    curl -L https://raw.github.com/pageauc/sonic-track/master/setup.sh | bash

From a computer logged into the RPI via ssh(Putty) session use mouse to highlight command above, right click, copy.  
Then select ssh(Putty) window, mouse right click, paste.  The command should 
download and execute the sonic-track github setup.sh script and install the sonic-track.  
This install can also be done directly on an Internet connected Raspberry Pi via a console or desktop terminal session and web browser.      
Note - a raspbian apt-get update and upgrade will be performed as part of install 
so it may take some time if these are not up-to-date

#### or Manual Install   
From logged in RPI SSH session or console terminal perform the following.

    wget https://raw.github.com/pageauc/sonic-track/master/setup.sh
    chmod +x setup.sh
    ./setup.sh

### How to Run
Default is console only display. Use Nano to Edit config.py variable window_on = True
to display the opencv tracking window on GUI desktop. See other variables
and descriptions for additional variable customization settings.
From SSH session, console or GUI desktop terminal session execute the following commands 

    cd ~/sonic-track
    ./sonic-track.sh   
    
### sonic-track.py - Basic concept of tracking moving objects
This Demo program detects motion in the field of view using opencv3 commands and returns movement 
contours above a minimum size and returns the x,y,h,w of the movement contours. These values are then
sent to sonic-pi via psonic.py and pythonosc.  sonic-track.sh can run in a SSH terminal 
session only. The sonic-pi gui will be launched via xauth display commands.  Make sure the 
Raspberry Pi Jessie OS pixel GUI desktop is running.  This demo needs to run on
a quad core raspberry pi with the latest Jessie build installed.
 
* Motion Track Demo YouTube Video http://youtu.be/09JS7twPBsQ  
* GitHub Repo https://github.com/pageauc/sonic-track

### Introduction
I did quite a bit of searching on the internet, github, etc, but could not
at the time find a similar python picamera implementation that returns x,y coordinates of
the moving objects in the frame although some came close.  This demo app sends 
movement data to sonic-pi via psonic.py and pythonosc.  You will need a pi camera and a powered speaker
connected to the Raspberry Pi audio/video plug via appropriate cables.
I thought it would be interesting to point the camera at a fish tank or other source of
random movement to see what sounds are generated.  This is just a very basic
setup but more elaborate sonic-pi sound generation algorithms are possible. 

### Prerequisites

* Requires a quad core Raspberry Pi computer running with an up-to-date raspbian Jessie distro
* RPI camera module installed and configured. 
* Dependencies will be installed via setup.sh depending on your previous installs.  
* opencv3 is required and can be installed via setup.sh menu picks (if required)
* sonic-pi is installed as part of the Jessie full install distro (not Lite)
* Powered speaker including cables between RPI 3.5 mm audio/video plug and speaker
You will also need a speaker plugged into the 3.5mm audio/video jack
similar to these cables https://www.adafruit.com/product/2881 
or https://www.amazon.com/Parts-Express-3-5mm-Plug-Cable/dp/B0007V6JCK  
these are also available from other vendors.  Just google 3.5mm audio/video jack
* You may also need a cable similar to this 
https://www.amazon.com/P316-06N-6-Inch-Stereo-Splitter-Adapter/dp/B00M5FKF9E/ref=sr_1_1?ie=UTF8&qid=1490056641&sr=8-1&keywords=35+mm+rca+audio+cable
depending on the powered speaker audio IN connection requirements.

### Change Settings

Edit the config.py file and set variables as per comments

    cd ~./sonic-track
    nano config.py
    
or run settings menu pick from setup.sh

    cd ~./sonic-track
    ./setup.sh
        
This interface runs under python sonic psonic.py.  For more information about this
see https://github.com/gkvoelkl/python-sonic  

To change the notes algorithm Edit sonic-track.py

    cd ~./sonic-track
    nano sonic-track.py    

Edit the play_notes function to change how the x, y, h, w motion variables interface with the sonic-pi sound generation      
per the psonic.py python library        
        
### Credits  
Some of this code is based on a YouTube tutorial by
Kyle Hounslow using C here https://www.youtube.com/watch?v=X6rPdRZzgjg

Thanks to Adrian Rosebrock jrosebr1 at http://www.pyimagesearch.com 
for the PiVideoStream Class code available on github at
https://github.com/jrosebr1/imutils/blob/master/imutils/video/pivideostream.py

## ---------- Other Raspberry Pi Projects Based on Motion Tracking ------------

### speed-camera.py - Object (vehicle) speed camera based on motion tracking
Tracks vehicle speeds or other moving objects in real time and records image 
and logs data. Now improved using threading for video stream and clipping of 
area of interest for greater performance.  
* GitHub Repo https://github.com/pageauc/rpi-speed-camera
* YouTube Speed Camera Video https://youtu.be/eRi50BbJUro  
* RPI forum post https://www.raspberrypi.org/forums/viewtopic.php?p=1004150#p1004150  

### cam-track.py - Tracks camera x y movements
Uses a clipped search image rectangle to search subsequent video stream images and returns
the location. Can be used for tracking camera x y movements for stabilization,
robotics, Etc.  
* GitHub Repo https://github.com/pageauc/rpi-cam-track
* YouTube Cam-Track Video https://www.youtube.com/edit?video_id=yjA3UtwbD80   
* Code Walkthrough YouTube Video https://youtu.be/lkh3YbbNdYg        
* RPI Forum Post https://www.raspberrypi.org/forums/viewtopic.php?p=1027463#p1027463   

### hotspot-game.py - A simple motion tracking game
The game play involves using streaming video of body motion to get as many hits 
as possible inside shrinking boxes that randomly move around the screen. 
Position the camera so you can see body motions either close or standing. 
Pretty simple but I think kids would have fun with it and they just might 
take a look at the code to see how it works, change variables or game logic.      
* GitHub hotspot-game Repo https://github.com/pageauc/hotspot-game 
* YouTube Hotspot Gam Video https://youtu.be/xFl3lmbEO9Y       
* RPI Forum Post https://www.raspberrypi.org/forums/viewtopic.php?p=1026124#p1026124   

## ----------------------------------------------------------------------------
  
Have Fun   
Claude Pageau    
YouTube Channel https://www.youtube.com/user/pageaucp   
GitHub Repo https://github.com/pageauc

