from imports import *
from PIL import Image, ImageTk

# Variables
image_paths = []

def open_file():
    files = filedialog.askopenfilenames(title='select images')
    if len(files) < 2:
        messagebox.showerror("Error", "please select at least two images")
        return
    for file in files:
        image_paths.append(file)
    messagebox.showinfo("Success", "Selected {} images".format(len(files)))

def stitch_images():
    paths = image_paths
    if len(paths) < 2:
        messagebox.showerror("Error", "please select at least two images")
        return
    
    images = []
    for path in paths:
        img = cv.imread(path)
        if img is None:
            messagebox.showerror("Error", "Could not open/read the image {}".format(path)) 
            return
        images.append(img)
    
    stitcher = cv.Stitcher_create()
    status, pano = stitcher.stitch(images)
    print("Stitching status:", status)

    if status != cv.Stitcher_OK:
        messagebox.showerror("Error", "Image Stiching Failed")
        return
    
    display_image(pano)
    messagebox.showerror("Success", "Image Stitching success")

def display_image(image):
    rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)
    imgTk = ImageTk.PhotoImage(image=pil_image)
    panel.config(image=imgTk)
    panel.image = imgTk

root = tk.Tk()
root.title("Image Stitcher")
root.geometry("1000x600")
panel = tk.Label(root)
panel.pack(padx=10,pady=10)

open_button = tk.Button(root, text="Open Images", command=open_file)
open_button.pack(pady=10)

stitch_button = tk.Button(root, text="Stitch images", command=stitch_images)
stitch_button.pack(pady=10)

root.mainloop()