# Config.py file for motion-track.py

# Display Settings
debug = True        # Set to False for no data display
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
CAMERA_WIDTH = 160
CAMERA_HEIGHT = 128
big_w = int(CAMERA_WIDTH * WINDOW_BIGGER)
big_h = int(CAMERA_HEIGHT * WINDOW_BIGGER)      
CAMERA_HFLIP = False
CAMERA_VFLIP = False
CAMERA_ROTATION=0
CAMERA_FRAMERATE = 5
FRAME_COUNTER = 1000

# Motion Tracking Settings
MIN_AREA = 50       # excludes all contours less than or equal to this Area
THRESHOLD_SENSITIVITY = 25
BLUR_SIZE = 10
