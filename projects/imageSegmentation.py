import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import filedialog, Button, Label

def select_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    image = cv.imread(filename=file_path)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    segment_image(image)

def segment_image(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    _, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    kernel = np.ones((3,3), np.uint8)
    opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=2)
    sure_background_area = cv.dilate(opening, kernel, iterations=3)
    dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
    _, sure_foreground = cv.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    sure_foreground = np.uint8(sure_foreground)
    unknown = cv.subtract(sure_background_area, sure_foreground)
    ret, markers = cv.connectedComponents(sure_foreground)
    markers += 1
    markers[unknown == 255] = 0
    markers = cv.watershed(image, markers)
    image[markers == -1] = [255, 0, 0]

    display_segmented_image(image)

def display_segmented_image(image):
    cv.imshow("Segmented Image", cv.cvtColor(image, cv.COLOR_RGB2BGR))
    cv.waitKey(0)
    cv.destroyAllWindows()

root = tk.Tk()
root.title("Image Segmentation via waterfall")
root.geometry("1000x700")

label = Label(root, text="Select image")
label.pack(pady=10)

select_button = Button(root, text="Select Image", command=select_image)
select_button.pack(pady=10)

root.mainloop()