from imports import *

class MotionDetectionApp:
    # Motion Detection App with open cv
    
    def __init__(self, root):
        # Initialize Everything
        self.root = root
        self.root.title("Motion Detector")
        self.root.geometry("1000x600")

        # Tkinter Buttons
        self.start_button = ttk.Button(root, text="Start Detecting", command=self.start_detection)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(root, text="Stop detecting", command=self.stop_detection)
        self.stop_button.pack(pady=10)

        self.status_label = ttk.Label(root, text="Status: Not Running")
        self.status_label.pack(pady=10)

        # Application state variables
        self.running = False  # Controls if motion detection is active
        self.webcam = None    # OpenCV video capture object

    def start_detection(self):
        """
        Start the motion detection process
        - Enables the detection loop
        - Updates GUI button states
        - Calls the main detection function
        """
        self.running = True  # Enable the detection loop
        self.start_button.configure(state=tk.DISABLED)  # Disable start button
        self.stop_button.configure(state=tk.NORMAL)     # Enable stop button
        self.status_label.configure(text="Status: Running")  # Update status
        self.detect_motion()  # Start the main detection loop

    def stop_detection(self):
        """
        Stop the motion detection process
        - Disables the detection loop
        - Updates GUI button states
        - Releases camera resources
        """
        self.running = False  # Disable the detection loop
        self.start_button.configure(state=tk.NORMAL)   # Enable start button
        self.stop_button.configure(state=tk.DISABLED)  # Disable stop button
        self.status_label.configure(text="Status: Not running")  # Update status
        
        # Clean up camera resources
        if self.webcam:
            self.webcam.release()  # Release the camera
            cv.destroyAllWindows()  # Close all OpenCV windows
    
    def detect_motion(self):
        """
        Main motion detection algorithm using frame differencing technique
        
        How it works:
        1. Capture initial frame and convert to grayscale
        2. Apply Gaussian blur to reduce noise
        3. For each new frame:
           - Convert to grayscale and blur
           - Calculate absolute difference with previous frame
           - Apply threshold to create binary image
           - Find contours of motion areas
           - Draw bounding boxes around significant motion
        4. Update previous frame for next iteration
        """
        
        # Initialize camera capture (using camera index 1 for Mac's built-in camera)
        self.webcam = cv.VideoCapture(1)
        
        # Capture the first frame to use as reference
        _, prev_frame = self.webcam.read()
        
        # Convert to grayscale for easier processing
        # Grayscale reduces complexity and improves motion detection accuracy
        prev_gray_image = cv.cvtColor(prev_frame, cv.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise and smooth the image
        # Kernel size (21,21) determines blur intensity - larger = more blur
        prev_blur_image = cv.GaussianBlur(prev_gray_image, (21, 21), 0)

        # Main detection loop - runs until stopped
        while self.running:
            # Capture current frame from camera
            _, frame = self.webcam.read()
            
            # Convert current frame to grayscale
            current_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            
            # Apply same blur to current frame for consistency
            current_gray_and_blur = cv.GaussianBlur(current_gray, (21, 21), 0)

            # Calculate absolute difference between previous and current frame
            # This highlights areas where motion occurred
            delta_frame = cv.absdiff(prev_blur_image, current_gray_and_blur)
            
            # Apply threshold to create binary image (black/white)
            # Values above 30 become white (255), below become black (0)
            thresh = cv.threshold(delta_frame, 30, 255, cv.THRESH_BINARY)[1]
            
            # Dilate the threshold image to fill gaps in motion areas
            # This connects broken parts of moving objects
            thresh = cv.dilate(thresh, None, iterations=2)

            # Find contours (outlines) of motion areas
            # RETR_EXTERNAL: Only external contours (not nested)
            # CHAIN_APPROX_SIMPLE: Compresses contour points
            contours, _ = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

            # Process each detected motion contour
            for contour in contours:
                # Filter out small contours (noise) - only keep significant motion
                # Area < 1000 pixels is considered noise
                if cv.contourArea(contour=contour) < 1000:
                    continue
                
                # Get bounding rectangle coordinates for the motion area
                (x,y,w,h) = cv.boundingRect(contour)
                
                # Draw green rectangle around the motion area
                # color=(0,255,0) is green in BGR format
                cv.rectangle(img=frame, pt1=(x,y), pt2=(x + w, y + h), color=(0,255,0), thickness=2) 
            
            # Display the processed frame with motion detection
            cv.imshow("Motion Detection", frame)
            
            # Wait for key press (1ms delay) and get key code
            key = cv.waitKey(1) & 0xFF

            # Exit if 'q' is pressed or detection is stopped
            if key == ord('q') or (self.running == False):
                break

            # Update previous frame for next iteration
            # This is crucial - we compare each frame to the previous one, not the first frame
            prev_blur_image = current_gray_and_blur.copy()

        # Clean up when detection stops
        self.stop_detection()

if __name__ == "__main__":
    """
    Main entry point of the application
    Creates the main window and starts the GUI event loop
    """
    root = tk.Tk()  # Create the main Tkinter window
    app = MotionDetectionApp(root)  # Initialize our motion detection app
    root.mainloop()  # Start the GUI event loop (keeps the app running)