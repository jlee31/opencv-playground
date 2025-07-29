import cv2 as cv
import os

img = cv.imread(os.path.join('.', 'Resources', 'Photos', 'lady.jpg'))

print(img.shape)

# adding lines
img_line = cv.line(img= img, pt1=(100,100), pt2=(500,500), color=(0,255,0), thickness=3)
# adding rectangles
img_rect = cv.rectangle(img = img, pt1= (200, 350), pt2= (400, 600), color=(255,0,0), thickness=5) # -1 thickness will completely fill
# adding circle
img_circ = cv.circle(img = img, center=(150,150), thickness=2, radius=100, color=(0,0,255))
# adding text
img_text = cv.putText(img=img, text='HELLO BRO', org = (40, 80), fontFace= cv.FONT_HERSHEY_COMPLEX, fontScale= 2, color=(0,0,0), thickness=4)

cv.imshow('image', img)
cv.waitKey(0)

# https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html
