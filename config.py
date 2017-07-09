# Config.py file for motion-track.py
# requires sonic_track 0.4 or greater 

# Display Settings
# ----------------
verbose = True      # Set to False for no data display
window_on = False   # Set to True displays opencv windows (GUI desktop reqd)
diff_window_on = False  # Show OpenCV image difference window
thresh_window_on = False  # Show OpenCV image Threshold window
SHOW_CIRCLE = True  # show a circle otherwise show bounding rectancle on window
CIRCLE_SIZE = 8     # diameter of circle to show motion location in window
LINE_THICKNESS = 1  # thickness of bounding line in pixels
WINDOW_BIGGER = 1   # Resize multiplier for Movement Status Window
                    # if gui_window_on=True then makes opencv window bigger
                    # Note if the window is larger than 1 then a reduced frame rate will occur            

# Camera Settings
# ---------------
WEBCAM = False        # default = False False=PiCamera True=USB WebCamera
                    
# Web Camera Settings
WEBCAM_SRC = 0        # default = 0   USB opencv connection number
WEBCAM_WIDTH = 320    # default = 320 USB Webcam Image width
WEBCAM_HEIGHT = 240   # default = 240 USB Webcam Image height
WEBCAM_HFLIP = False  # default = False USB Webcam flip image horizontally
WEBCAM_VFLIP = False  # default = False USB Webcam flip image vertically

# Pi Camera Settings 
CAMERA_WIDTH = 320     # Image stream width for opencv motion scanning default=320
CAMERA_HEIGHT = 240    # Image stream height for opencv motion scanning  default=240
CAMERA_FRAMERATE = 10  # frame rate for video stream default=55 90 max for V1 cam. V2 can be higher
CAMERA_ROTATION = 0    # Rotate camera image valid values are 0, 90, 180, 270
CAMERA_VFLIP = False   # Flip the camera image vertically if required
CAMERA_HFLIP = False   # Flip the camera image horizontally if required

# Motion Tracking Settings
# ------------------------
MIN_AREA = 100     # excludes all contours less than or equal to this Area
THRESHOLD_SENSITIVITY = 25
BLUR_SIZE = 10

# python-sonic midi notes settings
# --------------------------------
notes_delay = 0.5        # seconds delay between notes played 
octave_area_on = True    # True = area changes octave  False = default_octave

# Lists of notes in each octave range
# -----------------------------------
octave_0 = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ] 
octave_1 = [ 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23 ] 
octave_2 = [ 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35 ] 
octave_3 = [ 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47 ] 
octave_4 = [ 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59 ] 
octave_5 = [ 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71 ] 
octave_6 = [ 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83 ] 
octave_7 = [ 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95 ] 
octave_8 = [ 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107 ] 
octave_9 = [ 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119 ]
octave_10 = [ 120, 121, 122, 123, 124, 125, 126, 127 ]

# Default octave if octave_area_on = False
# ----------------------------------------
default_octave = octave_5   # set default value for octave if not controlled by area
default_octave_number = 5   # set default octave number per above setting

# contour area greater than to trigger each octave range
# ------------------------------------------------------
octave_0_trig = 9000    # sq_px contour greater than area to trigger this octave
octave_1_trig = 8000    # sq_px contour greater than area to trigger this octave
octave_2_trig = 6000    # sq_px contour greater than area to trigger this octave
octave_3_trig = 4000    # sq_px contour greater than area to trigger this octave
octave_4_trig = 2000    # sq_px contour greater than area to trigger this octave
octave_5_trig = 1000    # sq_px contour greater than area to trigger this octave
octave_6_trig = 500     # sq_px contour greater than area to trigger this octave
octave_7_trig = 200     # sq_px contour greater than area to trigger this octave
octave_8_trig = 100     # sq_px contour greater than area to trigger this octave
octave_9_trig = 50      # sq_px contour greater than area to trigger this octave
octave_10_trig = 40     # sq_px contour greater than area to trigger this octave

