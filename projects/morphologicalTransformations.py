from imports import *
from tkinter import Scale, HORIZONTAL, Button

# Initialize

root = tk.Tk()
root.title("Morphological Transformations")
root.geometry("1000x600")

# Global variables
img = None
img_display = None

def load_image():
    global img, img_display
    file_path = filedialog.askopenfilename()
    img = cv.imread(file_path, cv.IMREAD_COLOR)
    if img is not None:
        apply_transformation()
    
def apply_transformation(*args):
    global img, img_display

    if img is None:
        return
    
    kernel_size = kernel_scale.get()
    operation = var.get()

    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    if operation == "Erosion":
        transformed_img = cv.erode(src=img, kernel=kernel, iterations=1)
    elif operation == "Dilation":
        transformed_img = cv.dilate(src=img, kernel=kernel, iterations=1)
    elif operation == "Opening":
        transformed_img = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
    elif operation == "Closing":
        transformed_img = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)
    elif operation == "Gradient":
        transformed_img = cv.morphologyEx(img, cv.MORPH_GRADIENT, kernel)
    elif operation == "Top Hat":
        transformed_img = cv.morphologyEx(img, cv.MORPH_TOPHAT, kernel)
    elif operation == "Black Hat":
        transformed_img = cv.morphologyEx(img, cv.MORPH_BLACKHAT, kernel)

    img_display = transformed_img
    cv.imshow("Image", img_display)
    cv.waitKey(0)
    cv.destroyAllWindows()

options = ["Erosion", "Dilation", "Opening", "Closing", "Gradient", "Top Hat", "Black Hat"]

# Menu

var = tk.StringVar(root)
var.set(options[0])
operation_menu = tk.OptionMenu(root, var, *options)
operation_menu.pack()

# Slider for Kernel

kernel_scale = Scale(root, from_=1, to=20, orient=HORIZONTAL, label="Kernel Size")
kernel_scale.set(5)
kernel_scale.pack()

# Load Image
load_button = Button(root, text="Load Image", command=load_image)
load_button.pack()

# 
kernel_scale.bind('<ButtonRelease-1>', lambda x: apply_transformation())
var.trace("w", apply_transformation)

# Start
root.mainloop()
cv.destroyAllWindows()