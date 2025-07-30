import cv2 as cv
import mediapipe as mp
import os
import argparse

def process_image(image, face_detection):
    img_toRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    output = face_detection.process(img_toRGB)
    # print(output.detections)

    H, W, _ = image.shape

    for detection in output.detections:
        print("hi")
        location_data = detection.location_data
        bounding_box = location_data.relative_bounding_box

        x1, y1, width, height = bounding_box.xmin, bounding_box.ymin, bounding_box.width, bounding_box.height
        x1 = int(x1 * W)
        y1 = int(y1 * H)
        w = int(width * W)
        h = int(height * H)
        print("checkpoint 2")
        print(f"Original coordinates: x1={x1}, y1={y1}, w={w}, h={h}")
        
        # Ensure coordinates are within image bounds
        x1 = max(0, x1)
        y1 = max(0, y1)
        w = min(w, W - x1)
        h = min(h, H - y1)
        print("checkpoint 3")
        print(f"Adjusted coordinates: x1={x1}, y1={y1}, w={w}, h={h}")
        
        # Check if region is valid
        if w <= 0 or h <= 0:
            print("Invalid region size, skipping...")
            continue
            
        try:
            # blur the face region   
            face_region = img[y1: y1 + h, x1: x1 + w, :]
            print(f"Face region shape: {face_region.shape}")
            blurred_face = cv.blur(face_region, ksize=(30,30))
            img[y1: y1 + h, x1: x1 + w, :] = blurred_face
            print("face region successfully blurred")
        except Exception as e:
            print(f"Error during blur: {e}")
        
        # cv.imshow('Face Blurring MACHINE', img)
        # cv.waitKey(0)
    return img

####################

args = argparse.ArgumentParser()
args.add_argument("--mode", default='image')
args.add_argument("--filePath", default='./Resources/Photos/old_man.png')
args = args.parse_args()

####################

# read image
filepath = os.path.join('.', 'Resources', 'Photos', 'old_man.png')
img_raw = cv.imread(filepath)
img = cv.resize(img_raw, (500,500))

# detect the faces
mp_face = mp.solutions.face_detection
with mp_face.FaceDetection(min_detection_confidence = 0.5, model_selection = 0) as face_detection:

    if args.mode in ["image"]:
        img = cv.imread(args.filePath)
        img = process_image(img, face_detection)
        cv.imwrite(os.path.join('.', 'Resources', 'Photos', 'blurred_image2.png'), img)

    elif args.mode in ["video"]:
        cap = cv.VideoCapture(args.filePath)
        ret, frame = cap.read()
        output_video = cv.VideoWriter(os.path.join('.', 'Resources', 'Videos', 'output.mp4'),
                                      cv.VideoWriter_fourcc(*'MP4V'),
                                      25,
                                      (frame.shape[1], frame.shape[0])) 
        while ret:
            frame = process_image(frame, face_detection)
            output_video.write(frame)
            ret , frame = cap.read() 
        cap.release()
        output_video.release()

    elif args.mode in ["webcam"]:
        webcam = cv.VideoCapture(0)
        ret, frame = webcam.read()
        while ret:
            frame = process_image(frame, face_detection)
            cv.imshow('Webcam', frame)
            cv.waitKey(25)
            ret , frame = webcam.read()
        webcam.release()
