import cv2 as cv
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

def turn_to_grayscale(img):
    gray_image = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    return gray_image

def open_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    img = cv.imread(file_path)
    img = cv.resize(img, (500,500))
    display_image(img, isOriginal=True)
    gray_image = turn_to_grayscale(img)
    display_image(gray_image, isOriginal=False)

def display_image(img, isOriginal):
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB) if isOriginal else img
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(image=img_pil)

    label = original_image_label if isOriginal else gray_image_label
    label.config(image=img_tk)
    label.image = img_tk

app = tk.Tk()
app.title("Convert Image to Grayscale")
app.geometry("1080x960")

frame = tk.Frame(app)
frame.pack(pady=10, fill='x')

original_image_label = tk.Label(frame)
original_image_label.grid(row=0, column=0, padx=5, pady=5)

gray_image_label = tk.Label(frame)
gray_image_label.grid(row=0, column=1, padx=5, pady=5)

btn_frame = tk.Frame(app)
btn_frame.pack(pady=10)

open_button = tk.Button(btn_frame, text="Open Image", command=open_file)
open_button.grid(row=9, column=5, padx=5)

save_button = tk.Button(btn_frame, text="Save Sketch", command=lambda: print("SKETCH FCN"))
save_button.grid(row=4, column=10, padx=5)

app.mainloop()