import cv2 as cv
import os
import numpy as np
import tkinter as tk

from tkinter import filedialog
from tkinter import messagebox

from PIL import Image, ImageTk

# Store the PIL Images
images = {"original": None, "sketch": None}

def open_file():
    filePath = filedialog.askopenfilename()
    if not filePath:
        return
    img = cv.imread(filePath)
    display_image(img, original = True)
    sketch_image = convert_to_sketch(img)
    display_image(sketch_image, original=False)

def convert_to_sketch(img):
    gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    inverted_image = cv.bitwise_not(gray_image)
    blurred_image = cv.GaussianBlur(inverted_image, (21,21), sigmaX=0, sigmaY=0)
    inverted_blur_image = cv.bitwise_not(blurred_image)
    sketch_image = cv.divide(gray_image, inverted_blur_image, scale=256.0)
    return sketch_image

def display_image(img, original):
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB) if original else img
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(image=img_pil)

    # Storing the Image into the dictionary
    if original:
        images["original"] = img_pil
    else:
        images["sketch"] = img_pil

    label = original_image_label if original else sketch_image_label
    label.config(image=img_tk)
    label.image = img_tk

def save_sketch():
    if images["sketch"] is None:
        messagebox.showerror("Error", "No sketch to save.")
        return

    sketch_filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if not sketch_filepath:
        return

    # Save the PIL image (sketch) to the file
    images["sketch"].save(sketch_filepath, "PNG")
    messagebox.showinfo("Saved", "Sketch saved to {}".format(sketch_filepath))


app = tk.Tk()
app.title('Pencil Sketch Converter')

frame = tk.Frame(app)
frame.pack(pady=10, padx=10)

original_image_label = tk.Label(frame)
original_image_label.grid(row=0, column=0, padx=5, pady=5)
sketch_image_label = tk.Label(frame)
sketch_image_label.grid(row=0, column=1, padx=5, pady=5)

btn_frame = tk.Frame(app)
btn_frame.pack(pady=10)

open_button = tk.Button(btn_frame, text="Open Image", command=open_file)
open_button.grid(row=0, column=0, padx=5)

save_button = tk.Button(btn_frame, text="Save Sketch", command=save_sketch)
save_button.grid(row=0, column=1, padx=5)

app.mainloop()
