import cv2 as cv
import os

img = cv.imread(os.path.join('.', 'Resources', 'Photos', 'lady.jpg'))

img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img3 = cv.cvtColor(img, cv.COLOR_RGB2BGR)
img4 = cv.cvtColor(img, cv.COLOR_RGB2HSV)

cv.imshow('image', img)
cv.imshow('img grey', img2)
cv.imshow('img bgr', img3)
cv.imshow('img hsv', img4)
cv.waitKey(0)