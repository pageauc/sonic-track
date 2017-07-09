#!/usr/bin/env python3

progname = "sonic_track.py"
ver = "ver 0.50"

print("%s %s using sonic-pi, pi-camera, python3 and OpenCV" % (progname, ver))
print("Loading Please Wait ....")

import os
mypath=os.path.abspath(__file__)       # Find the full path of this python script
baseDir=mypath[0:mypath.rfind("/")+1]  # get the path location only (excluding script name)
baseFileName=mypath[mypath.rfind("/")+1:mypath.rfind(".")]
progName = os.path.basename(__file__)

# Check for variable file to import and error out if not found.
configFilePath = baseDir + "config.py"
if not os.path.exists(configFilePath):
    print("ERROR - Missing config.py file - Could not find Configuration file %s" % (configFilePath))
    import urllib2
    config_url = "https://raw.github.com/pageauc/sound-track/master/config.py"
    print("   Attempting to Download config.py file from %s" % ( config_url ))
    try:
        wgetfile = urllib2.urlopen(config_url)
    except:
        print("ERROR - Download of config.py Failed")
        print("   Try Rerunning the sound-track-install.sh Again.")
        print("   or")
        print("   Perform GitHub curl install per Readme.md")
        print("   and Try Again")
        print("Exiting %s" % ( progName ))
        quit()
    f = open('config.py','wb')
    f.write(wgetfile.read())
    f.close()   
# Read Configuration variables from config.py file
from config import *

# import the necessary packages
import io
import time
import cv2

from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from psonic import *

# Setup global variables for notes
# Change this into a function to allow variable notes in octave range

#-----------------------------------------------------------------------------------------------  
class PiVideoStream:
    def __init__(self, resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=CAMERA_FRAMERATE, rotation=0, hflip=False, vflip=False):
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.rotation = rotation
        self.camera.framerate = framerate
        self.camera.hflip = hflip
        self.camera.vflip = vflip
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

#-----------------------------------------------------------------------------------------------  
def get_octave ( x, y, w, h ):
    area = w * h
    
    if octave_area_on:
        if area > octave_0_trig:
            notes_octave = octave_0
            octave = 0        
        if area > octave_1_trig:
            notes_octave = octave_1
            octave = 1        
        if area > octave_2_trig:
            notes_octave = octave_2
            octave = 2
        elif area > octave_3_trig:
            notes_octave = octave_3           
            octave = 3
        elif area > octave_4_trig:
            notes_octave = octave_4    
            octave = 4
        elif area > octave_5_trig:
            notes_octave = octave_5    
            octave = 5
        elif area > octave_6_trig:
            notes_octave = octave_6    
            octave = 6
        elif area > octave_7_trig:
            notes_octave = octave_7 
            octave = 7
        elif area > octave_8_trig:
            notes_octave = octave_8
            octave = 8
        elif area > octave_9_trig:
            notes_octave = octave_9
            octave = 9
        elif area > octave_10_trig:
            notes_octave = octave_10
            octave = 10
        else:
            notes_octave = default_octave
            octave = default_octave_number
    else:
        notes_octave = default_octave
        octave = default_octave_number
    
    # split screen into horz and vert note zones    
    notes_total = len(notes_octave)
    horiz_zone = int(CAMERA_WIDTH / (notes_total-1))
    vert_zone = int(CAMERA_HEIGHT /(notes_total-1))
    x_idx = int( x / horiz_zone )
    y_idx = int( y / vert_zone )
    
    note1 = notes_octave[x_idx]
    note2 = notes_octave[y_idx]

    print("Octave=%i note1=%i note2=%i xy(%i,%i) xy(idx=%i,%i) area(%i*%i)=%i" %( octave, note1, note2, x, y, x_idx, y_idx, w, h, area ))
    
    return note1, note2   
    
#-----------------------------------------------------------------------------------------------  
def play_notes(x, y, w, h):

   use_synth(BEEP)
   # use_synth(PROPHET)

   note1, note2 = get_octave(x, y, w, h)
  
   play([note1, note2])
   sleep(notes_delay)

#-----------------------------------------------------------------------------------------------  
def sonic_track():
    print("Initializing Camera ....")
    # Save images to an in-program stream
    # Setup video stream on a processor Thread for faster speed
    vs = PiVideoStream().start()
    vs.camera.rotation = CAMERA_ROTATION
    vs.camera.hflip = CAMERA_HFLIP
    vs.camera.vflip = CAMERA_VFLIP
    time.sleep(2.0)    
    if window_on:
        print("press q to quit opencv display")
    else:
        print("press ctrl-c to quit")
    if octave_area_on:
        print("octave_area_on=True  Octave changes by area")
    else:
        print("octave_area_on=False Octave default is 5")    
    print("Start Motion Tracking ....")
    cx = 0
    cy = 0
    cw = 0
    ch = 0
    frame_count = 0
    start_time = time.time()
    # initialize image1 using image2 (only done first time)
    image2 = vs.read()     
    image1 = image2
    grayimage1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    first_image = False    
    still_scanning = True
    while still_scanning:
        image2 = vs.read()        
        # initialize variables         
        motion_found = False
        biggest_area = MIN_AREA
        # At this point the image is available as stream.array
        # Convert to gray scale, which is easier
        grayimage2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        # Get differences between the two greyed, blurred images
        differenceimage = cv2.absdiff(grayimage1, grayimage2)
        differenceimage = cv2.blur(differenceimage,(BLUR_SIZE,BLUR_SIZE))
        # Get threshold of difference image based on THRESHOLD_SENSITIVITY variable
        retval, thresholdimage = cv2.threshold( differenceimage, THRESHOLD_SENSITIVITY, 255, cv2.THRESH_BINARY )         
        try:
            thresholdimage, contours, hierarchy = cv2.findContours( thresholdimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )        
        except:       
            contours, hierarchy = cv2.findContours( thresholdimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )         
        # Get total number of contours
        total_contours = len(contours)
        # save grayimage2 to grayimage1 ready for next image2
        grayimage1 = grayimage2
        # find contour with biggest area
        for c in contours:
            # get area of next contour
            found_area = cv2.contourArea(c)
            # find the middle of largest bounding rectangle
            if found_area > MIN_AREA:
                (x, y, w, h) = cv2.boundingRect(c)
                cx = x + w/2
                cy = y + h/2
                play_notes(cx, cy, w, h)
                cw = w
                ch = h
                
        if motion_found:
            if window_on:
                # show small circle at motion location
                if SHOW_CIRCLE:
                    cv2.circle(image2,(cx,cy),CIRCLE_SIZE,(0,255,0), LINE_THICKNESS)
                else:
                    cv2.rectangle(image2,(cx,cy),(x+cw,y+ch),(0,255,0), LINE_THICKNESS)                  
            if verbose:
                print("Motion at cx=%3i cy=%3i  total_Contours=%2i  biggest_area:%3ix%3i=%5i" % (cx ,cy, total_contours, cw, ch, biggest_area))

        if window_on:
            if diff_window_on:
                cv2.imshow('Difference Image',differenceimage) 
            if thresh_window_on:
                cv2.imshow('OpenCV Threshold', thresholdimage)
            if WINDOW_BIGGER > 1:  # Note setting a bigger window will slow the FPS
                image2 = cv2.resize( image2,( big_w, big_h ))                             
            cv2.imshow('Movement Status  (Press q in Window to Quit)', image2)
            
            # Close Window if q pressed while movement status window selected
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                vs.stop()
                print("End Motion Tracking")
                still_scanning = False

#-----------------------------------------------------------------------------------------------    
if __name__ == '__main__':
    try:
        sonic_track()
    finally:
        print("")
        print("+++++++++++++++++++++++++++++++++++")
        print("%s %s - Exiting" % (progname, ver))
        print("+++++++++++++++++++++++++++++++++++")
        print("")                                



