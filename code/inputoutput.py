import os
import cv2

# read images / videos
image_path = os.path.join('.', 'Resources', 'Photos', 'cat.jpg')
img = cv2.imread(image_path)

video_path = os.path.join('.', 'Resources', 'Videos', 'dog.mp4')
video = cv2.VideoCapture(video_path)

webcam = cv2.VideoCapture(0)


# write images

cv2.imwrite(os.path.join('.', 'Resources', 'Photos', 'cat_out.jpg'), img)

# visualize images

cv2.imshow('image', img)
cv2.waitKey(0)
'''
ret = True
while ret:
    ret, frame = video.read()
    cv2.imshow('video', frame)

    if cv2.waitKey(1) == ord('q'):
        break
 
video.release()
'''
ret = True
while True:
    ret, frame = webcam.read()
    cv2.imshow('webcam', frame)
    if cv2.waitKey(1) == ord('q'):
        break

webcam.release()

cv2.destroyAllWindows()