import cv2 as cv
import os

img = cv.imread(os.path.join('.', 'Resources', 'Photos', 'birds.jpg'))

img_grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

ret, trace = cv.threshold(img_grey, 127, 255, cv.THRESH_BINARY_INV) # take anything higher than 127 to 0

contours, hierarchy = cv.findContours(image=trace, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    print(cv.contourArea(cnt))
    if cv.contourArea(cnt) > 200:
        # cv.drawContours(img, cnt, -1, (0,255,0), 1) # draw lines over each image
        x1, y1, w, h = cv.boundingRect(cnt)
        cv.rectangle(img, (x1,y1),(x1 + w,y1 + h), (0,255,0), 1)

cv.imshow('img', img)
cv.imshow('img gray', img_grey)
cv.imshow('trace', trace)
cv.waitKey(0)
