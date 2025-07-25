# pip install opencv-contrib-python
# pip install caer
 
import cv2 as cv
import sys

def image():
    img = cv.imread(cv.samples.findFile("Resources/Photos/cat.jpg"))
    
    if img is None:
        sys.exit("Could not read the image.")
    
    cv.imshow("Display window", img)
    k = cv.waitKey(0)
    
    if k == ord("s"):
        cv.imwrite("Resources/Photos/cat.jpg", img)

def video():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
    
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Display the resulting frame
        cv.imshow('frame', gray)
        if cv.waitKey(1) == ord('q'):
            break
    
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

video()