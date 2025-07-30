import cv2 as cv
import mediapipe as mp
import os

# read image
img_raw = cv.imread(os.path.join('.', 'Resources', 'Photos', 'old_man.png'))
img = cv.resize(img_raw, (500,500))

# Check if image was loaded successfully
if img is None:
    print("Error: Could not load the image!")
    print("Checking if file exists...")
    image_path = os.path.join('.', 'Resources', 'Photos', 'old_man.png')
    print(f"Looking for image at: {os.path.abspath(image_path)}")
    if os.path.exists(image_path):
        print("File exists but cv2.imread failed")
    else:
        print("File does not exist!")
    exit()

print(f"Image loaded successfully! Shape: {img.shape}")
H, W, _ = img.shape

# detect the faces
mp_face = mp.solutions.face_detection
with mp_face.FaceDetection(min_detection_confidence = 0.5, model_selection = 0) as face_detection:
    img_toRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    output = face_detection.process(img_toRGB)
    # print(output.detections)

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

# Save Image
cv.imwrite(os.path.join('.', 'Resources', 'Photos', 'blurred_image.png'), img)
