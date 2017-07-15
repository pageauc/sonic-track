# Raspberry Pi sonic-track.py a Sonic-pi Motion Track Demo
#### Tracks camera motion contours x,y,w,h values and generates sounds via sonic-pi.  
#### Uses pi-camera or webcam, python3, Opencv3, python-sonic, pythonosc, sonic-pi, powered speaker or HDMI TV

### NEW Release 0.91 Adds drums and restructures code and variables and adds option for zone grid lines on GUI

#### YouTube Video (motion activated menus https://youtu.be/PQjpskPAtR0
#### YouTube Video sonic-track into https://youtu.be/RCIUlv431E0

### Introduction
This demo app sends camera movement tracking data to sonic-pi music program.  sonic-track sends data to sonic-pi via psonic.py and pythonosc.
You will need a pi camera and a powered speaker connected to the Raspberry Pi audio/video plug via appropriate cables or you can attach RPI
to an HDMI TV via HDMI cable and sound will redirect to TV speakers.
I thought it would be interesting to point the camera at a fish tank or other source of
video movement to see what sounds are generated. You can also stand in front of the camera and generate sounds via body movements.

#### Some ideas I would like to work on

* Air drum eg bongo drum feature activated by body movement  (0.90 Added air drums)
* Simon type sound motion game to try to repeat a series of notes using body movement
 ( see hotspot game https://github.com/pageauc/hotspot-game )
* Implement bird call type game to use motion tracking to pick the bird associated with
 a sound from an on screen image of different birds. I have a poke-pi demo that allows displaying images on screen (not published)
 it allows for interactively taking an image of a toy or object then you can use the small icon in the motion tracking
 environment to do something.  I was visualizing something like pokemon
* Same as birds idea above but for any animals Eg farmyard or wild animals.
* Control a device and give audio feed back.  Eg higher sound for higher settings.

This program demo is a very basic setup but more elaborate sonic-pi sound generation algorithms are possible.

### How to Install

#### Quick Install   
Easy Install of sonic-track onto a Raspberry Pi Computer with latest Raspbian.
This is a whiptail menu system that allows install of opencv3 if required 

    curl -L https://raw.github.com/pageauc/sonic-track/master/setup.sh | bash

From a computer logged into the RPI via ssh (Putty) session use mouse to highlight command above, right click, copy.  
Then select ssh(Putty) window, mouse right click, paste.  The command should 
download and execute the sonic-track github setup.sh script and install sonic-track files and set permissions.  
This install can also be done directly on an Internet connected Raspberry Pi via a console or desktop terminal session and web browser.      
***Note*** - A raspbian apt-get update and upgrade will be performed as part of install 
so it may take some time if these are not up-to-date.

#### Manual Install   
From logged in RPI SSH session or console terminal perform the following.

    wget https://raw.github.com/pageauc/sonic-track/master/setup.sh
    chmod +x setup.sh
    ./setup.sh

### Opencv3 Install (if required)
sonic-track.py requires opencv3 to be installed on the latest RPI Jessie disto.
I have written a menu driven install script called cv3-setup.sh.  Use this if
you do not have opencv3 already installed. cv3-setup.sh menu picks allow updating,
installing dependencies, downloads, cmake, compile and make install of opencv 3.0.0.
I tried opencv 3.2.0 but had errors so it is best to stick with 3.0.0 per this script.
To Run the whiptail menu setup script.  From a logged in ssh or terminal session run

    cd ~/sonic-track
    ./cv3-setup.sh    
 
You will be asked to reboot at certain steps.  

More information is available   
here http://www.pyimagesearch.com/2015/10/26/how-to-install-opencv-3-on-raspbian-jessie/ 
    
### How to Run
Default is SSH or Terminal console only display. Make sure pixel desktop is
 enabled and logged in.  This can be done from raspi-config setting.
This is required for the sonic-track.sh to start sonic-pi on the desktop from
 an ssh only session.

Use Nano to Edit config.py variable settings. Select PiCamera or USB web camera
 depending on what you have installed or want to use. 
You should set the appropriate camera hflip, vflip as appropriate.
You can customize the synthPicks.  This is a comma delimited list of entries
 from the synthList above.  You can select any number and arrange them in any order. 
This list is used to to switch synth when motion is detected in the hotspot area
 (usually top/left corner)  You can also select a default_octave from the list
 of octave's above. You may also want to look at notesSleepOn, notesSleepVarOn, 
 notesSleep, notenotes_midi, octave triggers, Etc. See other variables and
 comments for additional variable customization settings.    
From SSH session, console or GUI desktop terminal session execute the following commands.
Make sure a speaker is connected to the pi before starting.

    cd ~/sonic-track
    ./sonic-track.sh   

To display opencv window on Raspberry Pi desktop set config.py variable below. 
    
    cd ~/sonic-track
    nano config.py
    
#### GUI RPI Desktop display video
With a display, keyboard and mouse attached to the RPI, Login to the Pixel Desktop

Use desktop menu to open a termina session.  The use nano to set the following
config.py variable then ctrl-x y to save change(s)

    cd ~/sonic-track
    nano config.py
    
edit the following setting the ctrl-x y to save
    
    windowOn = True

You can either start sonic-pi from the desktop the in the terminal window start sonic-track.py

or from the desktop terminal session run

    ./sonic-track.sh
    
### Change Settings

Edit the config.py file and set variables as per comments

    cd ~./sonic-track
    nano config.py
 
The play_notes function uses the motion contour center and width and height eg x, y, h, w motion variables.
These values are used to generate notes, noteSleep and/or change octave based on contour area.  Sound values are send
to sonic-pi interface.  Sounds can be changed using synth settings per config.py synthPicks.  The reference numbers
are from the synthList and the synthPicks list can contain any number of values separated by commas and
 arranged in any order.  These can be changed when sonic-track.sh is running my creating movement in the hotspot area
(default is top left corner 1/5 of the screen height and width. 
        
For more information about psonic see https://github.com/gkvoelkl/python-sonic    
and midi values see  http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm

To change how the notes algorithm works you would need to change sonic-track.py programing.  This will
require reprogramming how notes are generated via x,y,w,h values.  

    cd ~./sonic-track
    nano sonic-track.py    

### Prerequisites
* Recomend a quad core Raspberry Pi computer running with an up-to-date Raspbian Jessie distro
* RPI camera module or USB Web Cam installed/connected configured and tested to work. 
* Dependencies will be installed via setup.sh depending on your previous installs.  
* opencv3 is required and can be installed via cv3-setup.sh on menubox.sh menu pick (if required)
* sonic-pi is installed as part of the Jessie full install distro (not Lite)
* Optional Powered speaker including cables between RPI 3.5 mm audio/video plug and speaker if not using HDMI TV

You will also need an HDMI TV and Cable to the RPI or a speaker plugged into the 3.5mm audio/video jack 
similar to these cables https://www.adafruit.com/product/2881 
or https://www.amazon.com/Parts-Express-3-5mm-Plug-Cable/dp/B0007V6JCK  
these are also available from other vendors.  Just google 3.5mm audio/video jack
* You may also need a cable similar to this 
https://www.amazon.com/P316-06N-6-Inch-Stereo-Splitter-Adapter/dp/B00M5FKF9E/ref=sr_1_1?ie=UTF8&qid=1490056641&sr=8-1&keywords=35+mm+rca+audio+cable
depending on the powered speaker audio IN connection requirements.

### sonic-track.py - Basic concept of tracking moving objects
This Demo program detects motion in the field of view using opencv3 commands and returns movement 
contours above a minimum size and returns the x,y,h,w of the movement contours. These values are then
sent to sonic-pi via psonic.py and pythonosc.  sonic-track.sh can run in a SSH terminal 
session only. The sonic-pi gui will be launched via xauth display commands.  Make sure the 
Raspberry Pi Jessie OS pixel GUI desktop is running.  This demo needs to run on
a quad core raspberry pi with the latest Jessie build installed.
 
* Motion Track Demo YouTube Video http://youtu.be/09JS7twPBsQ   
* YouTube sonic-track demo https://youtu.be/RCIUlv431E0
* GitHub Repo https://github.com/pageauc/sonic-track

### Enhancements List

* Save motion notes to a csv file
* Read from a video file and generate notes based on motion tracking
* Read csv file and replay previous notes or read from another data file and convert to
note ranges required for input
* Create alternate configuration settings via separate config.py files.  This would allow
changing how notes are generated.
* Setup a method to easily change synth settings  (implemented pickList)

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

