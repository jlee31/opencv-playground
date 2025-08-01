import cv2 as cv
import tkinter as tk
from tkinter import ttk, filedialog, Button, Label

img1 = None
img2 = None

def select_image_1():
    global img1, file_path1
    file_path1 = filedialog.askopenfilename()
    if file_path1:
        img1 = cv.imread(file_path1, cv.IMREAD_GRAYSCALE)
        label_img1.config(text="Image1: {}".format(file_path1.split('/')[-1]))

def select_image_2():
    global img2, file_path2
    file_path2 = filedialog.askopenfilename()
    if file_path2:
        img2 = cv.imread(file_path2, cv.IMREAD_GRAYSCALE)
        label_img2.config(text="Image2: {}".format(file_path2.split('/')[-1]))

def feature_matching():
    if img1 is None or img2 is None:
        return
    orb = cv.ORB_create()

    keyPoints1, descriptors1 = orb.detectAndCompute(img1, None)
    keyPoints2, descriptors2 = orb.detectAndCompute(img2, None)

    brute_force = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    matches = brute_force.match(descriptors1, descriptors2)

    matches = sorted(matches, key = lambda x:x.distance)

    img_matches = cv.drawMatches(img1=img1, keypoints1=keyPoints1, img2=img2, keypoints2=keyPoints2, matches1to2=matches[:50], outImg=None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    cv.imshow("Feature Matching", img_matches)
    cv.waitKey(0)
    cv.destroyAllWindows()

root = tk.Tk()
root.title("Feature Matching")
root.geometry("1000x700")



btn_select_image1 = Button(root, text="Select Image 1", command=select_image_1)
btn_select_image1.pack()

label_img1 = Label(root, text="Image 1: Not Selected")
label_img1.pack()

btn_select_image2 = Button(root, text="Select Image 2", command=select_image_2)
btn_select_image2.pack()

label_img2 = Label(root, text="Image 2: Not Selected")
label_img2.pack()

btn_match_features = Button(root, text="Match features", command=feature_matching)
btn_match_features.pack()

root.mainloop()