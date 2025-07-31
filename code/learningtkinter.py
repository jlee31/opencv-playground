# quickly learning tkinter
import cv2 as cv
import os
import numpy as np
import tkinter as tk

from tkinter import filedialog
from tkinter import messagebox

from PIL import Image, ImageTk

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

open_button = tk.Button(btn_frame, text="Open Image", command=print("hello"))
open_button.grid(row=0, column=0, padx=5)

save_button = tk.Button(btn_frame, text="Save Sketch", command=print("bye"))
save_button.grid(row=0, column=1, padx=5)

app.mainloop()