from imports import *
from pyzbar.pyzbar import decode
from datetime import datetime
import os

def scan_barcode(frame ,log_results=False, log_file="scanned_barcodes.txt"):
    gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    barcodes = decode(gray_img)
    scanned_data = []
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        points = np.array([barcode.polygon], np.int32)
        points = points.reshape((-1,1,2))
        # drawing a polygon
        cv.polylines(frame, [points], True, (0,255,0), 3)
        rect = barcode.rect
        cv.putText(frame, '{} ({})'.format(barcode_data, barcode_type), (rect[0], rect[1]),
                   cv.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.9, (255,0,0), 2)
        scanned_data.append((barcode_data, barcode_type))
        if log_results:
            save_to_file(barcode_data, barcode_type, log_file)
        return frame, scanned_data
    
def save_to_file(data, barcode_type, file_path):
    with open(file_path, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write("{}, {}, {}\n".format(timestamp, data, barcode_type))

def start_scanner():
    webcam = cv.VideoCapture(0)
    log_file = "scanned_barcodes.txt"
    while True:
        ret, frame = webcam.read()
        if not ret:
            break
        scanned_frame, scanned_data = scan_barcode(frame, log_results=True, log_file=log_file)
        cv.imshow("Barcode Scanner", scanned_frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    webcam.release()
    cv.destroyAllWindows()
    messagebox.showinfo("Scanner Closed", "Scanned data saved to {}".format(log_file))

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png, *.jpg, *.jpeg")])
    if file_path:
        image = cv.imread(file_path)
        scanned_image, scanned_data = scan_barcode(image)
        cv.imshow("Barcode Scanner", scanned_image)
        if scanned_data:
            save_option = messagebox.askyesno("Save Results", "Do you want to save these results?")
            if save_option:
                save_results_to_file(scanned_data, file_path)
        cv.waitKey(0)
        cv.destroyAllWindows()

def save_results_to_file(scanned_data, source):
    log_file = "scanned_results_{}.txt".format(os.path.basename(source))
    with open(log_file, 'w') as f:
        for data, barcode_type in scanned_data:
            f.write("{}, {}".format(data, barcode_type))
    messagebox.showinfo("REsults Saved", "Scanned Results saved to {}".format(log_file))

def view_log_file():
    log_file = "scanned_barcodes.txt"
    if not os.path.exists(log_file):
        messagebox.showwarning("No Logs", "No log file found. Start scanning to generate logs")
        return
    with open(log_file, 'r') as f:
        logs = f.readlines()
    log_window = tk.Toplevel(app)    
    log_window.title("Scanned Logs")
    log_text = tk.Text(log_window, wrap="word", height=20, width=60)
    log_text.insert("1.0", ''.join(logs))
    log_text.config(state='disabled')
    log_text.pack(padx=10, pady=10)

app = tk.Tk()
app.title("Barcode Scanner")
app.geometry("1000x600")

start_button = tk.Button(app, text="Start Webcam Scanner", command=start_scanner)
start_button.pack(pady=10)

open_file_button = tk.Button(app, text="Select Image File", command=select_file)
open_file_button.pack(pady=10)

view_log_button = tk.Button(app, text="View Scan Logs", command=view_log_file)
view_log_button.pack(pady=10)

# Footer
footer_label = tk.Label(app, text="Press 'q' to exit the webcam scanner.", fg="blue")
footer_label.pack(pady=5)

app.mainloop()