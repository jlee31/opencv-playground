import cv2 as cv
import os
import numpy as np
# Edge detection

img = cv.imread(os.path.join('.', 'Resources', 'Photos', 'basketball.png'))

img_edge = cv.Canny(img, 100, 200)
img_edge_d = cv.dilate(img_edge, np.ones((3, 3), dtype=np.int8))
img_edge_e = cv.erode(img_edge_d, np.ones((3, 3), dtype=np.int8))


cv.imshow('img', img_edge)
cv.imshow('img_edge_d', img_edge_d)
cv.imshow('img_edge_e', img_edge_e)
cv.waitKey(0)