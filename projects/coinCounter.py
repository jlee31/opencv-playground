import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, Label, Scale, Button, HORIZONTAL

def process_image(image, blur_kernel_size, threshold_value, erosion_iterations, final_threshold_value):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (blur_kernel_size, blur_kernel_size), 0)

    _, thresh = cv.threshold(blurred, threshold_value, 255, cv.THRESH_BINARY)

    kernel = np.ones((5, 5), np.uint8)
    eroded = cv.erode(thresh, kernel, iterations=erosion_iterations)

    eroded_blurred = cv.GaussianBlur(eroded, (9, 9), 0)
    _, final_thresh = cv.threshold(eroded_blurred, final_threshold_value, 255, cv.THRESH_BINARY)

    contours, _ = cv.findContours(final_thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    coin_contours = [cnt for cnt in contours if cv.contourArea(cnt) > 100]

    output_image = image.copy()
    for cnt in coin_contours:
        (x, y), radius = cv.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)
        cv.circle(output_image, center, radius, (0, 255, 0), 2)

    coin_count = len(coin_contours)
    return output_image, coin_count

def select_image():
    global processed_image

    file_path = filedialog.askopenfilename()
    if not file_path:
        messagebox.showerror("Error", "Please select a proper file")
        return

    blur_kernel_size = blur_slider.get()
    threshold_value = threshold_slider.get()
    erosion_iterations = erosion_slider.get()
    final_threshold_value = final_threshold_slider.get()

    if blur_kernel_size % 2 == 0:
        blur_kernel_size += 1

    processed_image, coin_count = process_image(
        cv.imread(file_path),
        blur_kernel_size,
        threshold_value,
        erosion_iterations,
        final_threshold_value,
    )

    if processed_image is not None:
        cv.imshow("Coin Counting MACHINE", processed_image)
        cv.waitKey(0)
        cv.destroyAllWindows()
        messagebox.showinfo("Coin Count", f'Number of Coins Detected: {coin_count}')

def save_results():
    if 'processed_image' not in globals():
        messagebox.showerror("Error", "No processed image to save.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"),
                                                        ("JPEG files", "*.jpg"),
                                                        ("All files", "*.*")])
    if file_path:
        cv.imwrite(file_path, processed_image)
        messagebox.showinfo("Saved", "Image saved successfully!")

app = tk.Tk()
app.title("Coin Counting")
app.geometry("500x450")

blur_label = Label(app, text="Set the Blur Kernel Size")
blur_label.pack(pady=5)

blur_slider = Scale(app, from_=3, to=31, resolution=2, orient=HORIZONTAL)
blur_slider.set(5)
blur_slider.pack(pady=10)

threshold_label = Label(app, text="Threshold Value")
threshold_label.pack(pady=5)

threshold_slider = Scale(app, from_=1, to=255, orient=HORIZONTAL)
threshold_slider.set(50)
threshold_slider.pack(pady=10)

erosion_label = Label(app, text="Erosion Iterations")
erosion_label.pack(pady=5)

erosion_slider = Scale(app, from_=1, to=10, orient=HORIZONTAL)
erosion_slider.set(5)
erosion_slider.pack(pady=10)

final_threshold_label = Label(app, text="Final Threshold Value")
final_threshold_label.pack(pady=5)

final_threshold_slider = Scale(app, from_=1, to=255, orient=HORIZONTAL)
final_threshold_slider.set(255)
final_threshold_slider.pack(pady=10)

select_image_btn = Button(app, text="Select Image", command=select_image)
select_image_btn.pack(pady=10)

save_results_btn = Button(app, text="Save results", command=save_results)
save_results_btn.pack(pady=10)

app.mainloop()
