import cv2 as cv
import os

################################

# resizing
img = cv.imread(os.path.join('.', 'Resources', 'Photos', 'cat.jpg'))

resized_img = cv.resize(img, (320,214))

print(img.shape)
print(resized_img.shape)
cv.imshow('img', img)
# cv.imshow('resized_img', resized_img)



################################

# cropping

cropped_img = img[0:214,0:320]
cv.imshow('cropped image', cropped_img)

cv.waitKey(0)

####################################

