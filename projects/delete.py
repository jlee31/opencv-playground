import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter

class GlitchArtGenerator:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("TITLE")
        self.app.geometry("1000x700")  # Increased height to accommodate buttons

        # Create button frames first
        self.btn_frame = tk.Frame(self.app)
        self.btn_frame.pack(pady=5)

        self.effect_frame = tk.Frame(self.app)
        self.effect_frame.pack(pady=5)

        # Create canvas frame and canvas after buttons
        self.canvas_frame = tk.Frame(self.app)
        self.canvas_frame.pack(pady=10)

        # Reduced canvas size to leave room for buttons
        self.canvas = tk.Canvas(self.canvas_frame, width=700, height=450, bg='gray90')
        self.canvas.pack()

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
            button.pack(side=tk.LEFT, padx=3)
            print(f"Button {text} created.")

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
            button = tk.Button(self.effect_frame, text=text, command=command)
            button.pack(side=tk.LEFT, padx=3)
    
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("JPEG files", "*.jpg;*.jpeg"),
            ("PNG files", "*.png"),
            ("GIF files", "*.gif"),
            ("All files", "*.*")
        ])
        if file_path:
            self.original_image = cv.imread(filename=file_path)
            self.current_image = self.original_image.copy()
            self.show_image(self.current_image)
            self.undo_stack.clear()
            self.redo_stack.clear()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you wish to quit?"):
            self.app.destroy()

    def show_image(self, image):
        image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_pil = image_pil.resize((700,450), Image.LANCZOS)  # Match canvas size
        image_tk = ImageTk.PhotoImage(image_pil)

        self.canvas.delete("all")  # Clear previous image
        self.canvas.create_image(0,0, anchor='nw', image=image_tk)
        self.canvas.image_tk = image_tk
        
    def check_image(self):
        if self.current_image is None:
            messagebox.showerror("Error", "No Image Loaded")
            return True
        return False

    def undo_image(self):
        if len(self.undo_stack) > 0:
            self.redo_stack.append(self.current_image.copy())
            self.current_image = self.undo_stack.pop()
            self.show_image(self.current_image)

    def add_to_undo_stack(self):
        self.undo_stack.append(self.current_image.copy())
        self.redo_stack.clear()

    def redo_image(self):
        if len(self.redo_stack) > 0:
            self.undo_stack.append(self.current_image.copy())
            self.current_image = self.redo_stack.pop()
            self.show_image(self.current_image)

    def reset_image(self):
        if self.check_image():
            return 
        
        if self.original_image is not None:
            self.add_to_undo_stack()
            self.current_image = self.original_image.copy()
            self.show_image(self.current_image)

    def save_image(self):
        if self.current_image is None:
            messagebox.showerror("Error", "No Image to Save")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg"), ("BMP files", "*.bmp")])
        if file_path:
            cv.imwrite(filename=file_path, img=self.current_image)  # Fixed: use current_image instead of file_path
            messagebox.showinfo("Success", f'Image saved at {file_path}')
    

    def adjust_brightness(self):
        if self.check_image():
            return
        factor = simpledialog.askfloat("Input", "Enter Brightness Factor (From 0.1 to 2)", minvalue=0.1, maxvalue=2)
        if factor is not None:
            self.add_to_undo_stack()
            image_pil = Image.fromarray(cv.cvtColor(self.current_image, cv.COLOR_BGR2RGB))
            enhancer = ImageEnhance.Brightness(image_pil)
            enhanced_image = enhancer.enhance(factor)
            self.current_image = cv.cvtColor(np.array(enhanced_image), cv.COLOR_RGB2BGR)
            self.show_image(self.current_image)

    def adjust_saturation(self):
        if self.check_image():
            return
        factor = simpledialog.askfloat("Input", "Enter Brightness Factor (From 0.0 to 2)", minvalue=0.0, maxvalue=2)
        if factor is not None:
            self.add_to_undo_stack()
            image_pil = Image.fromarray(cv.cvtColor(self.current_image, cv.COLOR_BGR2RGB))
            enhancer = ImageEnhance.Color(image_pil)
            enhanced_image = enhancer.enhance(factor)
            self.current_image = cv.cvtColor(np.array(enhanced_image), cv.COLOR_RGB2BGR)
            self.show_image(self.current_image)

    def adjust_contrast(self):
        if self.check_image():
            return
        factor = simpledialog.askfloat("Input", "Enter Brightness Factor (From 0.1 to 2)", minvalue=0.1, maxvalue=2)
        if factor is not None:
            self.add_to_undo_stack()
            image_pil = Image.fromarray(cv.cvtColor(self.current_image, cv.COLOR_BGR2RGB))
            enhancer = ImageEnhance.Contrast(image_pil)
            enhanced_image = enhancer.enhance(factor)
            self.current_image = cv.cvtColor(np.array(enhanced_image), cv.COLOR_RGB2BGR)
            self.show_image(self.current_image)
            
    def glitch_image(self):  # Fixed: removed unnecessary image parameter
        if self.check_image():
            return
        
        intensity = simpledialog.askinteger("Input", "Enter Glitch Intensity (1-20)", minvalue=1, maxvalue=20)
        if intensity is not None:
            self.add_to_undo_stack()
            glitched_image = self.apply_glitch(self.current_image, intensity)
            self.current_image = glitched_image
            self.show_image(self.current_image)
    
    def apply_glitch(self, image, intensity):
            glitched_image = image.copy()
            height, width, _ = image.shape
            for _ in range(intensity):
                offset = np.random.randint(-10, 11, size=3)
                slice_height = np.random.randint(height//20, height//5)
                start_row = np.random.randint(0, height - slice_height)
                glitched_image[start_row:start_row+slice_height] = np.roll(glitched_image[start_row:start_row+slice_height], offset, axis = 1)
            return glitched_image
                
    def apply_blur(self):
        if self.check_image():
            return
        factor = simpledialog.askfloat("Input", "Enter Brightness Factor (From 1 to 10)", minvalue=1, maxvalue=10)
        if factor is not None:
            self.add_to_undo_stack()
            image_pil = Image.fromarray(cv.cvtColor(self.current_image, cv.COLOR_BGR2RGB))
            blurred_image = image_pil.filter(ImageFilter.GaussianBlur(radius=factor))
            self.current_image = cv.cvtColor(np.array(blurred_image), cv.COLOR_RGB2BGR)
            self.show_image(self.current_image)

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

if __name__ == "__main__":
    GlitchArtGenerator()