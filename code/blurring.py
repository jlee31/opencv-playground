import os
import cv2 as cv

img = cv.imread(os.path.join('.', 'Resources', 'Photos', 'lady.jpg'))

k_size = 7 # the larger the value, the greater the blur
img2 = cv.blur(img, (k_size, k_size))
img3 = cv.GaussianBlur(img, (k_size, k_size), 3)
img4 = cv.medianBlur(img, k_size)

# cv.imshow('imgage', img)
# cv.imshow('imgage', img2)
cv.imshow('imgage', img4)
cv.waitKey(0)