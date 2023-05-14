import cv2
import random
import os

# Specify the directory to store the captured frames and extracted eyes
directory_path = "captured_frames"
eyes_directory_path = "extracted_eyes"

# Create the directories if they don't exist
os.makedirs(directory_path, exist_ok=True)
os.makedirs(eyes_directory_path, exist_ok=True)

# Open the video capture
cap = cv2.VideoCapture(0)

# Set video capture duration (in seconds)
capture_duration = 10

# Set the number of frames to capture
num_frames = 20

# Calculate the frame rate based on capture duration and number of frames
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

# Calculate the interval between frames
frame_interval = int(frame_rate / num_frames)

# Initialize variables
frames_captured = 0
frames_saved = 0

# Load the Haar cascade for eye detection
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# Read and discard some frames to allow the camera to stabilize
for _ in range(frame_rate * 2):
    cap.read()

# Start capturing frames
while frames_captured < frame_rate * capture_duration and frames_saved < num_frames:
    # Read a frame from the video capture
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect eyes in the frame
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(80, 80))

    # Iterate through the detected eyes
    for (x, y, w, h) in eyes:
        # Check if the detection is likely to be an eye based on its position and size
        if y < frame.shape[0] / 2 and w < frame.shape[1] / 2:
            # Extract the region of interest (ROI) corresponding to the eyes
            eye_roi = gray[y:y+h, x:x + w]
            
            

            # Generate a unique image file name
            image_filename = f"{eyes_directory_path}/303.{frames_saved}.jpg"

            # Save the extracted eye as a grayscale JPEG image
            cv2.imwrite(image_filename, eye_roi)

            # Increment the frame counter
            frames_saved += 1

            # Break the loop if the desired number of eye images is reached
            if frames_saved >= num_frames:
                break

    # Display the frame
    cv2.imshow("Capturing Frames", frame)

    # Increment the frame counter
    frames_captured += 1

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture
cap.release()







# Close all OpenCV windows
cv2.destroyAllWindows()
