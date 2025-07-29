import os
import cv2 as cv

img = cv.imread(os.path.join('.', 'Resources', 'Photos', 'lady.jpg'))

img2 = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

ret, thresh = cv.threshold(img2, 80, 255, cv.THRESH_BINARY)
# thresholds pixels less than 80 to 255

thresh = cv.blur(thresh, (10, 10))
ret, thresh = cv.threshold(thresh, 80, 255, cv.THRESH_BINARY)

cv.imshow('imgage', img)
cv.imshow('image blur', thresh)


img_text = cv.imread(os.path.join('.', 'Resources', 'Photos', 'handwritten.png'))
img_text_grey = cv.cvtColor(img_text, cv.COLOR_RGB2GRAY)
# ret2, thresh2 = cv.threshold(img_text_grey, 60, 255, cv.THRESH_BINARY)
# ^^^ the above threshold can remove the lighting
thresh2 = cv.adaptiveThreshold(img_text_grey, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
                               cv.THRESH_BINARY, 21, 30)
# Automatic threshold - works a lot better
# read the documentation to see the parameters, they tweak how the adaptive threshold works
# there should technically be thresholds to see how the thing changes (could use pygame)

cv.imshow('new text', thresh2)
cv.waitKey(0)