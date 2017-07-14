#!/usr/bin/env python3
progVer = "ver 0.83"
# Archived this older version on GitHub 

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

# Calculated Variables Should not need changing by user
####

# See if Web Cam is selected
if WEBCAM:
    CAMERA_WIDTH = WEBCAM_WIDTH
    CAMERA_HEIGHT = WEBCAM_HEIGHT

# Increase size of openCV display window
big_w = int(CAMERA_WIDTH * windowBigger)
big_h = int(CAMERA_HEIGHT * windowBigger)

# initialize hotspot area variables
synthHotxy = (int(CAMERA_WIDTH/synthHotSize),int(CAMERA_HEIGHT/synthHotSize))
octaveHotxy = (int(CAMERA_WIDTH/octaveHotSize),int(CAMERA_HEIGHT/octaveHotSize))

# split screen into horz and vert zones for note changes
octaveStart = octavePicks[0]
notesTotal = len(octaveList[octaveStart][1])
notesHorizZone = int(CAMERA_WIDTH / (notesTotal - 1)) # Calculate Zone Area index
notesVertZone = int(CAMERA_HEIGHT /(notesTotal - 1))
noteSleepMin = float(noteSleepMin)  # make sure noteSleepMin is a float

# Color data for OpenCV lines and text
cvBlue = (255,0,0)
cvGreen = (0,255,0)
cvRed = (0,0,255)
FONT_SCALE = .3             # OpenCV window text font size scaling factor default=.5 (lower is smaller)

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
    differenceImage = cv2.absdiff( grayimage1, grayimage2 )
    # Blur difference image to enhance motion vectors
    differenceImage = cv2.blur( differenceImage,(BLUR_SIZE,BLUR_SIZE ))
    # Get threshold of blurred difference image based on THRESHOLD_SENSITIVITY variable
    retval, thresholdImage = cv2.threshold( differenceImage, THRESHOLD_SENSITIVITY, 255, cv2.THRESH_BINARY )
    try:
        thresholdImage, contours, hierarchy = cv2.findContours( thresholdImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
    except:
        contours, hierarchy = cv2.findContours( thresholdImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

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
def playNotes( synthNow, octaveNow, moveData ):
    global menuLock
    global menuTime

    x, y, w, h = moveData[0], moveData[1], moveData[2], moveData[3]
    xZone = int( x / notesHorizZone)
    yZone = int( y / notesVertZone )

    # Add entries to synthPicks array in config.py for available session synths
    if synthHotOn:   # Screen Hot Spot Area changes synthPick if movement inside area
        if ( x < synthHotxy[0] and y < synthHotxy[1] ) and not menuLock:
            menuLock = True
            menuTime = time.time()
            synthNow += 1
            if synthNow > len(synthPicks) - 1:
                synthNow = 0
    synthCur = synthList[synthPicks[synthNow]]  # Select current synth from your synthPicks
    synthName = synthCur[1]       # Get the synthName from synthCur
    use_synth(Synth(synthName))   # Activate the selected synthName

    # Add entries to octavePicks array in config.py for available session octaves
    if octaveHotOn:   # Screen Hot Spot Area changes octavePick if movement inside area
        if ( x > CAMERA_WIDTH - octaveHotxy[0] and y < octaveHotxy[1] ) and not menuLock:
            menuLock = True
            menuTime = time.time()
            octaveNow += 1
            if octaveNow > len(octavePicks) - 1:
                octaveNow = 0
    octaveCur = octaveList[octavePicks[octaveNow]]  # Select current synth from your synthPicks
    octaveNotes = octaveCur[1]   # Get the synthName from synthCur
    note1 = octaveNotes[xZone]
    note2 = octaveNotes[yZone]

    if menuLock:
        if (time.time() - menuTime > 2) :
            menuLock = False  # unlock motion menu after two seconds

    if noteDoubleOn:      # Generate two notes based on contour x, y rather than one
        play([note1, note2])
    else:
        play(note1)

    if noteSleepVarOn:   # Vary note sleep duration based on screen height
        notePosDelay =  h/float( CAMERA_HEIGHT/noteSleepMax )
        if (notePosDelay < noteSleepMin):
            notePosDelay = noteSleepMin
        elif (notePosDelay > noteSleepMax):
            notePosDelay = noteSleepMax
        sleep(notePosDelay)
    else:       # Set fixed note sleep duration
        sleep(noteSleepMin)
        notePosDelay = noteSleepMin

    if verbose:
        print("Octave:%i  note1=%i  note2=%i  moveXY(%i,%i)  zoneXY(%i,%i)  cArea(%i*%i)=%i" %
                     ( octaveCur[0], note1, note2, x, y, xZone, yZone, w, h, w*h ))
        print("synth:%i %s  noteSleep=%.3f seconds" % (synthCur[0], synthName, notePosDelay))
    return synthNow, octaveNow

#-----------------------------------------------------------------------------------------------
def sonicTrack():
    global menuLock
    global menuTime
    menuTime = time.time()
    menuLock = False

    if windowOn:
        print("press q to quit opencv display")
    else:
        print("press ctrl-c to quit")
    print("Start Motion Tracking ....")
    # initialize image1 using image2 (only done first time)
    image2 = vs.read()
    image1 = image2
    grayimage1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    still_scanning = True
    synthNow = 0   # Initialize first synth selection from synthPicks
    octaveNow = 0  # Initialize first synth selection from
    while still_scanning:
        image2 = vs.read()
        grayimage2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        moveData = trackPoint(grayimage1, grayimage2)
        grayimage1 = grayimage2

        if moveData:   # Found Movement
            synthNow, octaveNow = playNotes(synthNow, octaveNow, moveData)
            if windowOn:
                cx = moveData[0]
                cy = moveData[1]
                # show small circle at motion location
                if SHOW_CIRCLE:
                    cv2.circle(image2,(cx,cy),CIRCLE_SIZE, cvGreen, LINE_THICKNESS)
                else:
                    cw = moveData[2]
                    ch = moveData[3]
                    cv2.rectangle(image2,(int(cx - cw/2),int(cy - ch/2)),(int(cx + cw/2), int(cy+ch/2)),
                                                          cvGreen, LINE_THICKNESS)

        if windowOn:
            if synthHotOn:    # Box top left indicating synthHotOn Area
                cv2.rectangle(image2,(0,0), synthHotxy, cvBlue, LINE_THICKNESS)
                synthText = synthList[synthPicks[synthNow]][1]
                cv2.putText( image2, synthText, (5, int(synthHotxy[1]/2)),
                                cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE , cvGreen, 1)
            if octaveHotOn:  # Box top right indicating synthHotOn Area
                cv2.rectangle(image2,(CAMERA_WIDTH - octaveHotxy[0], 0),
                                     (CAMERA_WIDTH - 1,octaveHotxy[1]), cvBlue, LINE_THICKNESS)
                octaveText = ("octave %i" % octavePicks[octaveNow])
                cv2.putText( image2, octaveText, (CAMERA_WIDTH - int(octaveHotxy[0] - 5), int(octaveHotxy[1]/2)),
                                cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE , cvGreen, 1)
            if windowDiffOn:
                cv2.imshow('Difference Image', differenceImage)
            if windowThreshOn:
                cv2.imshow('OpenCV Threshold', thresholdImage)
            if windowBigger > 1:  # Note setting a bigger window will slow the FPS
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

            sonicTrack()
    except KeyboardInterrupt:
        vs.stop()
        print("")
        print("+++++++++++++++++++++++++++++++++++")
        print("User Pressed Keyboard ctrl-c")
        print("%s %s - Exiting" % (progName, progVer))
        print("+++++++++++++++++++++++++++++++++++")
        print("")
        quit(0)