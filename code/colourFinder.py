import cv2 as cv
import numpy as np
from PIL import Image

# Constants
webcam = cv.VideoCapture(0)
YELLOW = [0,255,255]
GREEN  = (0,255,0)

def get_limits(color):
    c = np.uint8([[color]])  # BGR values
    hsvC = cv.cvtColor(c, cv.COLOR_BGR2HSV)

    hue = hsvC[0][0][0]  # Get the hue value

    # Handle red hue wrap-around
    if hue >= 165:  # Upper limit for divided red hue
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  # Lower limit for divided red hue
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit

def detect_colour(colour):
    # Function
    while True:
        ret, frame = webcam.read()

        # converting from BGR to HSV
        hsv_image = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        lower_limit, upper_limit = get_limits(color=colour)
        image_mask = cv.inRange(src=hsv_image, lowerb=lower_limit, upperb=upper_limit) 

        image_mask_toPillow = Image.fromarray(image_mask)

        bounding_box = image_mask_toPillow.getbbox()

        if bounding_box:
            x1, y1, x2, y2 = bounding_box
            cv.rectangle(frame, (x1, y1), (x2, y2), GREEN, 3)

        cv.imshow('Colour Finder', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    webcam.release()
    cv.destroyAllWindows()
    return

detect_colour(YELLOW)