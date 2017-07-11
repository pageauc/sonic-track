#!/usr/bin/env python3
progVer = "ver 0.70"

import os
mypath=os.path.abspath(__file__)       # Find the full path of this python script
baseDir=mypath[0:mypath.rfind("/")+1]  # get the path location only (excluding script name)
baseFileName=mypath[mypath.rfind("/")+1:mypath.rfind(".")]
progName = os.path.basename(__file__)

print("%s %s using sonic-pi, pi-camera, python3 and OpenCV" % (progName, progVer))
print("Loading Please Wait ....")

# Check for config variable file to import and error out if not found.
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

# See if Web Cam is selected
if WEBCAM:
    CAMERA_WIDTH = WEBCAM_WIDTH
    CAMERA_HEIGHT = WEBCAM_HEIGHT
big_w = int(CAMERA_WIDTH * WINDOW_BIGGER)
big_h = int(CAMERA_HEIGHT * WINDOW_BIGGER)

# initialize hotspot area variable
synthHotxy = (int(CAMERA_WIDTH/synthHotSize),int(CAMERA_HEIGHT/synthHotSize))
notesSleep = float(notesSleep)

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
class WebcamVideoStream:
    def __init__(self, CAM_SRC=WEBCAM_SRC, CAM_WIDTH=WEBCAM_WIDTH, CAM_HEIGHT=WEBCAM_HEIGHT):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = CAM_SRC
        self.stream = cv2.VideoCapture(CAM_SRC)
        self.stream.set(3,CAM_WIDTH)
        self.stream.set(4,CAM_HEIGHT)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                    return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

#-----------------------------------------------------------------------------------------------
def trackPoint(grayimage1, grayimage2):
    moveData = []   # initialize list of movementCenterPoints
    biggestArea = MIN_AREA
    # Get differences between the two greyed images
    differenceimage = cv2.absdiff( grayimage1, grayimage2 )
    # Blur difference image to enhance motion vectors
    differenceimage = cv2.blur( differenceimage,(BLUR_SIZE,BLUR_SIZE ))
    # Get threshold of blurred difference image based on THRESHOLD_SENSITIVITY variable
    retval, thresholdimage = cv2.threshold( differenceimage, THRESHOLD_SENSITIVITY, 255, cv2.THRESH_BINARY )
    try:
        thresholdimage, contours, hierarchy = cv2.findContours( thresholdimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
    except:
        contours, hierarchy = cv2.findContours( thresholdimage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

    if contours != ():
        for c in contours:
            cArea = cv2.contourArea(c)
            if cArea > biggestArea:
                biggestArea = cArea
                ( x, y, w, h ) = cv2.boundingRect(c)
                cx = int(x + w/2)   # x center point of contour
                cy = int(y + h/2)   # y center point of contour
                moveData = [cx, cy, w, h]
    return moveData

#-----------------------------------------------------------------------------------------------
def get_octave ( x, y, w, h ):  
# Needs more work to improve since not working well
# Will look at a pick list similar to synthPick
                              
    area = w * h
    if octave_area_on:
        if area > octave_0_trig:
            notes_octave = octave_0
            octave = 3
        if area > octave_1_trig:
            notes_octave = octave_1
            octave = 3
        if area > octave_2_trig:
            notes_octave = octave_2
            octave = 4
        elif area > octave_3_trig:
            notes_octave = octave_3
            octave = 4
        elif area > octave_4_trig:
            notes_octave = octave_4
            octave = 5
        elif area > octave_5_trig:
            notes_octave = octave_5
            octave = 5
        elif area > octave_6_trig:
            notes_octave = octave_6
            octave = 6
        elif area > octave_7_trig:
            notes_octave = octave_7
            octave = 6
        elif area > octave_8_trig:
            notes_octave = octave_8
            octave = 7
        elif area > octave_9_trig:
            notes_octave = octave_9
            octave = 7
        elif area > octave_10_trig:
            notes_octave = octave_10
            octave = 7
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
    if verbose:
        print("Octave=%i note1=%i note2=%i xy(%i,%i) xy(idx=%i,%i) area(%i*%i)=%i" %
                ( octave, note1, note2, x, y, x_idx, y_idx, w, h, area ))
    return note1, note2

#-----------------------------------------------------------------------------------------------
def play_notes(synthNow, x, y, w, h):

    # Add entries to synthPicks array in config.py for available session synths   
    if synthHotOn:   # Screen Hot Spot Area changes synthPick if movement inside area
        if ( x < synthHotxy[0] and y < synthHotxy[1] ):
            synthNow += 1
            if synthNow > len(synthPicks) - 1:
                synthNow = 0
    synthCur = synthList[synthPicks[synthNow]]  # Select current synth from your synthPicks
    synthName = synthCur[1]       # Get the synthName from synthCur 
    use_synth(Synth(synthName))   # Activate the selected synthName

    note1, note2 = get_octave(x, y, w, h)   # Generated notes based on screen x and y position

    if notesDoubleOn:      # Generate two notes rather than one
        play([note1, note2])
    else:
        play(note1)

    if notesSleepVarOn:   # Vary the note duration based on screen height
        notePosDelay =  h/float( CAMERA_HEIGHT/0.3 )
        if (notePosDelay < 0.1):
            notePosDelay = 0.1
        elif (notePosDelay > 0.3):
            notePosDelay = 0.3
        if verbose:
            print("synth:%i %s  sleep=%.3f seconds" % (synthCur[0], synthName, notePosDelay))
        sleep(notePosDelay)
    else:
        sleep(notesSleep)
    return synthNow
    
#-----------------------------------------------------------------------------------------------
def sonic_track():
    if windowOn:
        print("press q to quit opencv display")
    else:
        print("press ctrl-c to quit")
    if octave_area_on:
        print("octave_area_on=True  Octave changes by area")
    else:
        print("octave_area_on=False Octave default is 5")
    print("Start Motion Tracking ....")
    cx, cy, cw, ch = 0,0,0,0
    frame_count = 0
    start_time = time.time()
    # initialize image1 using image2 (only done first time)
    image2 = vs.read()
    image1 = image2
    grayimage1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    still_scanning = True
    synthNow = 0     # Initialize first synth selection from synthPicks
    while still_scanning:
        image2 = vs.read()
        grayimage2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        moveData = trackPoint(grayimage1, grayimage2)
        grayimage1 = grayimage2

        if moveData:   # Found Movement
            cx, cy, cw, ch = moveData[0], moveData[1], moveData[2], moveData[3]
            synthNow = play_notes(synthNow, cx, cy, cw, ch)

            if windowOn:
                # show small circle at motion location
                if SHOW_CIRCLE:
                    cv2.circle(image2,(cx,cy),CIRCLE_SIZE,(0,255,0), LINE_THICKNESS)
                else:
                    cv2.rectangle(image2,(cx,cy),(int(cx + cw/2),int(cy+ch/2)),(0,255,0), LINE_THICKNESS)

        if windowOn:
            if diff_window_on:
                cv2.imshow('Difference Image',differenceimage)
            if thresh_window_on:
                cv2.imshow('OpenCV Threshold', thresholdimage)
            if synthHotOn:    # Red Box indicating synthHotOn Area 
                cv2.rectangle(image2,(0,0), synthHotxy,(255,0,0), LINE_THICKNESS)                 
            if WINDOW_BIGGER > 1:  # Note setting a bigger window will slow the FPS
                image2 = cv2.resize( image2,( big_w, big_h ))
            cv2.imshow('Movement Status  (Press q in Window to Quit)', image2)

            # Close Window if q pressed while movement status window selected
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                vs.stop()
                print("End Motion Tracking")
                still_scanning = False
                quit()

#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        while True:
            # Save images to an in-program stream
            # Setup video stream on a processor Thread for faster speed
            if WEBCAM:   #  Start Web Cam stream (Note USB webcam must be plugged in)
                print("Initializing USB Web Camera ....")
                vs = WebcamVideoStream().start()
                vs.CAM_SRC = WEBCAM_SRC
                vs.CAM_WIDTH = WEBCAM_WIDTH
                vs.CAM_HEIGHT = WEBCAM_HEIGHT
                time.sleep(4.0)  # Allow WebCam to initialize
            else:
                print("Initializing Pi Camera ....")
                vs = PiVideoStream().start()
                vs.camera.rotation = CAMERA_ROTATION
                vs.camera.hflip = CAMERA_HFLIP
                vs.camera.vflip = CAMERA_VFLIP
                time.sleep(2.0)  # Allow PiCamera to initialize

            sonic_track()
    except KeyboardInterrupt:
        vs.stop()
        print("")
        print("+++++++++++++++++++++++++++++++++++")
        print("User Pressed Keyboard ctrl-c")
        print("%s %s - Exiting" % (progName, progVer))
        print("+++++++++++++++++++++++++++++++++++")
        print("")
        quit(0)
