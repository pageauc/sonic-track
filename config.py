# Config.py file for motion-track.py
# requires sonic_track 0.80 or greater

# Display Settings
# ----------------
verbose = True      # Set to False for no data display
windowOn = False    # Set to True displays opencv windows (GUI desktop reqd)

# Camera Settings
# ---------------
WEBCAM = False        # False=PiCamera True=USB WebCamera

# Web Camera Settings
WEBCAM_SRC = 0        # default= 0   USB opencv connection number
WEBCAM_WIDTH = 320    # default= 320 USB Webcam Image width
WEBCAM_HEIGHT = 240   # default= 240 USB Webcam Image height
WEBCAM_HFLIP = False  # default= False USB Webcam flip image horizontally
WEBCAM_VFLIP = False  # default= False USB Webcam flip image vertically

# Pi Camera Settings
CAMERA_WIDTH = 320     # Image stream width for opencv motion scanning default=320
CAMERA_HEIGHT = 240    # Image stream height for opencv motion scanning  default=240
CAMERA_VFLIP = False   # Flip the camera image vertically if required
CAMERA_HFLIP = False   # Flip the camera image horizontally if required
CAMERA_ROTATION = 0    # Rotate camera image valid values are 0, 90, 180, 270
CAMERA_FRAMERATE = 10  # frame rate for video stream default=55 90 max for V1 cam. V2 can be higher

# List of Available sythesizers and a reference number for adding items to synthPick list below
synthList = [
(0,'dull_bell'),
(1,'pretty_bell'),
(2,'square'),
(3,'pulse'),
(4,'subpulse'),
(5,'dtri'),
(6,'dpulse'),
(7,'fm'),
(8,'mod_fm'),
(9,'mod_saw'),
(10,'mod_dsaw'),
(11,'mod_sine'),
(12,'mod_tri'),
(13,'mod_pulse'),
(14,'supersaw'),
(15,'hoover'),
(16,'synth_violin'),
(17,'pluck'),
(18,'piano'),
(19,'growl'),
(20,'dark_ambience'),
(21,'dark_sea_horn'),
(22,'hollow'),
(23,'zawa'),
(24,'noise'),
(25,'gnoise'),
(26,'bnoise'),
(27,'cnoise'),
(28,'dsaw'),
(29,'tb303'),
(30,'blade'),
(31,'prophet'),
(32,'saw'),
(33,'beep'),
(34,'tri'),
(35,'dtri'),
(36,'pluck'),
(37,'chiplead'),
(38,'chipbass'),
(39,'chipnoise'),
(40,'tech_saws'),
(41,'sound_in'),
(42,'sound_in_stereo')
]
# Select synthPicks numbers above comman separated (any number or order)
synthPicks = [ 36, 17, 18, 31, 32 ]

# Currently selected synth for screen motion pick box
synthHotOn = True  # Turn on HotSpot to cycle through synthPicks
synthHotSize = 5   # Divide screen W,H by synthHotSize determines hotSpot Area W,H

# Lists of notes in each octave range
# -----------------------------------
octaveList = [
(0,[ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ]),
(1,[ 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23 ]),
(2,[ 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35 ]),
(3,[ 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47 ]),
(4,[ 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59 ]),
(5,[ 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71 ]),
(6,[ 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83 ]),
(7,[ 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95 ]),
(8,[ 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107 ]),
(9,[ 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119 ]),
(10,[ 120, 121, 122, 123, 124, 125, 126, 127 ])
]
# Select octavePicks numbers above comman separated (any number an order)
octavePicks = [ 4, 5, 6 ]

octaveHotOn = True   # Turn on HotSpot to cycle through octavePicks via motion hotspot
octaveHotSize = 5    # Division factor for cam image size xy to allocate to Hot Area

# python-sonic midi notes settings
# --------------------------------
noteSleepVarOn = True # default= True Turn On Variable notes sleep time based on screen y position
noteDoubleOn = False  # Play two notes rather than one per contour
noteSleepMin = 0.1     # default= 0.1 seconds delay between notes played
noteSleepMax = 0.4     # default= 0.4 max delay based on h of contour

# OpenCV Settings
# ---------------
MIN_AREA = 100      # Excludes all contours less than or equal to this Area
SHOW_CIRCLE = False # True= Show circle for movement, False= Show rectancle on screen
CIRCLE_SIZE = 5     # diameter of circle to show motion location in window
LINE_THICKNESS = 1  # thickness of bounding line in pixels
windowBigger = 2    # Image Resize multiplier for Images
windowDiffOn = False  # Show OpenCV image difference window
windowThreshOn = False  # Show OpenCV image Threshold window

# You should not have to change these settings
THRESHOLD_SENSITIVITY = 25
BLUR_SIZE = 10
