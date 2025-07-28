import os
import cv2

# read images
image_path = os.path.join('.', 'Resources', 'Photos', 'cat.jpg')
img = cv2.imread(image_path)

# write images

cv2.imwrite(os.path.join('.', 'Resources', 'Photos', 'cat_out.jpg'), img)

# visualize images

cv2.imshow('image', img)
cv2.waitKey(0)

 