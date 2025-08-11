import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter

class GlitchArtGenerator:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("TITLE")
        self.app.geometry("1000x600")

        self.canvas = tk.Canvas(self.app, width=800, height=600)
        self.canvas.pack(pady=10)

        self.btn_frame = tk.Frame(self.app)
        self.btn_frame.pack(pady=10)

        self.create_buttons()
        self.create_effect_options()

        self.original_image = None
        self.current_image = None
        self.undo_stack = []
        self.redo_stack = []

        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.app.mainloop()
    
    def create_buttons(self):
        buttons = [
            ("Load Image", self.load_image),
            ("Apply Glitch", self.glitch_image),
            ("Save Image", self.save_image),
            ("Undo", self.undo_image),
            ("Redo", self.redo_image),
            ("Reset", self.reset_image)
        ]

        for text, command in buttons:
            button = tk.Button(self.btn_frame, text=text, command=command)
            button.pack()

    def create_effect_options(self):
        effects = [
            ("Brightness", self.adjust_brightness),
            ("Contrast", self.adjust_contrast),
            ("Saturation", self.adjust_saturation),
            ("Blur", self.apply_blur),
            ("Sharpen", self.apply_sharpen),
            ("Pixilate", self.apply_pixels),
            ("Invert Colors", self.apply_invert),
            ("Add Noise", self.apply_noise),
            ("Vignette", self.apply_vignette),
            ("Retro Filter", self.apply_retro_filter)
        ]

        for text, command in effects:
            btn = tk.Button(self.effect_frame, text=text, command=command)
            btn.pack(tk.LEFT, padx=3)
    
    def load_image(self):
        pass

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you wish to quit?"):
            self.app.destroy(side=tk.LEFT, padx=5)

    def glitch_image(self):
        pass

    def undo_image(self):
        pass

    def redo_image(self):
        pass

    def reset_image(self):
        pass

    def adjust_brightness(self):
        pass

    def adjust_saturation(self):
        pass

    def apply_blur(self):
        pass

    def apply_sharpen(self):
        pass

    def apply_pixels(self):
        pass
    
    def apply_invert(self):
        pass
    
    def apply_noise(self):
        pass

    def apply_vignette(self):
        pass

    def apply_retro_filter(self):
        pass

