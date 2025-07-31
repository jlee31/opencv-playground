import cv2 as cv
import tkinter as tk
from tkinter import ttk

class LiveGrayScaleFilter():
    def __init__(self, root):
        self.root = root
        self.root.title("Live Gray Scale")
        self.run_filter = False
        self.setup_ui()
        self.webcam = cv.VideoCapture(0)

    def setup_ui(self):
        self.start_button = ttk.Button(self.root, text="Start", command=self.start_filtering_to_gray)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_filtering)
        self.stop_button.pack(pady=10)

    def start_filtering_to_gray(self):
        self.run_filter = True
        self.process_frames()

    def stop_filtering(self):
        self.run_filter = False
        cv.destroyAllWindows()

    def process_frames(self):
        if not self.run_filter:
            return
        ret, frame = self.webcam.read()
        if ret:
            gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            cv.imshow("Live Grayscale", gray_frame)
            cv.waitKey(20)
        self.root.after(10, self.process_frames)

    def on_closing(self):
        self.run_filter = False
        if self.webcam.isOpened():
            self.webcam.release()
        cv.destroyAllWindows()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LiveGrayScaleFilter(root)
    root.geometry("1000x600")
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()