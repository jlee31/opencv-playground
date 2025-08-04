from imports import *

class MotionDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Motion Detector")
        self.root.geometry("1000x600")

        self.start_button = ttk.Button(root, text="Start Detecting", command=self.start_detection)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(root, text="Stop detecting", command=self.stop_detection)
        self.stop_button.pack(pady=10)

        self.status_label = ttk.Label(root, text="Status: Not Running")
        self.status_label.pack(pady=10)

        self.running = False
        self.webcam = None

    def start_detection(self):
        self.running = True
        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)
        self.status_label.configure(text="Status: Running")
        self.detect_motion()

    def stop_detection(self):
        self.running = False
        self.start_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)
        self.status_label.configure(text="Status: Not running")
        if self.webcam:
            self.webcam.release()
            cv.destroyAllWindows()
    
    def detect_motion(self):
        self.webcam = cv.VideoCapture(1)
        _, prev_frame = self.webcam.read()
        prev_gray_image = cv.cvtColor(prev_frame, cv.COLOR_BGR2GRAY)
        prev_blur_image = cv.GaussianBlur(prev_gray_image, (21, 21), 0)

        while self.running:
            _, frame = self.webcam.read()
            current_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            current_gray_and_blur = cv.GaussianBlur(current_gray, (21, 21), 0)

            delta_frame = cv.absdiff(prev_blur_image, current_gray_and_blur)
            thresh = cv.threshold(delta_frame, 30, 255, cv.THRESH_BINARY)[1]
            thresh = cv.dilate(thresh, None, iterations=2)

            contours, _ = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                # Increase minimum area to filter out noise
                if cv.contourArea(contour=contour) < 1000:
                    continue
                (x,y,w,h) = cv.boundingRect(contour)
                cv.rectangle(img=frame, pt1=(x,y), pt2=(x + w, y + h), color=(0,255,0), thickness=2) 
            
            cv.imshow("Motion Detection", frame)
            key = cv.waitKey(1) & 0xFF

            if key == ord('q') or (self.running == False):
                break

            # Update the previous frame for next iteration
            prev_blur_image = current_gray_and_blur.copy()

        self.stop_detection()

if __name__ == "__main__":
    root = tk.Tk()
    app = MotionDetectionApp(root)
    root.mainloop()