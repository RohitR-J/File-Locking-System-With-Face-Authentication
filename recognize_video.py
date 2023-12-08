# login.py
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import os
import cv2
import imutils
import time
import pickle
import numpy as np
from imutils.video import FPS
from imutils.video import VideoStream
from PIL import Image, ImageTk
import sys

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize an empty list to store authorized users
authorized_users = []

# Read the authorized user names from the "authorized_users.txt" file
authorized_users_file = os.path.join(BASE_DIR, "authorized_users.txt")
with open(authorized_users_file, "r") as file:
    for line in file:
        authorized_users.append(line.strip())


# Create a new tkinter window for the authenticated user
def authenticated():
    boolean_value = True
    print(boolean_value)
    sys.exit(boolean_value)


# Load serialized face detector
print("Loading Face Detector...")
protoPath = os.path.join(BASE_DIR, "face_detection_model/deploy.prototxt")
modelPath = os.path.join(BASE_DIR, "face_detection_model/res10_300x300_ssd_iter_140000.caffemodel")
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# Load serialized face embedding model
print("Loading Face Recognizer...")
embedder = cv2.dnn.readNetFromTorch(os.path.join(BASE_DIR, "openface_nn4.small2.v1.t7"))

# Load the actual face recognition model along with the label encoder
recognizer_path = os.path.join(BASE_DIR, "output/recognizer.pickle")
label_encoder_path = os.path.join(BASE_DIR, "output/le.pickle")

with open(recognizer_path, "rb") as f:
    recognizer = pickle.load(f)

with open(label_encoder_path, "rb") as f:
    le = pickle.load(f)

# Initialize the video stream, then allow the camera sensor to warm up
print("Starting Video Stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# Start the FPS throughput estimator
fps = FPS().start()

# Create a tkinter window
root = tk.Tk()
root.title("Face Recognition")

# Create a label widget to display the video stream
label = tk.Label(root)
label.pack()


# Function to update the label with the current frame
def update_frame():
    frame = vs.read()
    frame = imutils.resize(frame, width=600)
    (h, w) = frame.shape[:2]

    imageBlob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)), 1.0, (300, 300),
        (104.0, 177.0, 123.0), swapRB=False, crop=False)

    authentication_result = "Not Authenticated"  # Default result

    detector.setInput(imageBlob)
    detections = detector.forward()

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            face = frame[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]

            if fW < 20 or fH < 20:
                continue

            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                                             (96, 96), (0, 0, 0), swapRB=True, crop=False)
            embedder.setInput(faceBlob)
            vec = embedder.forward()

            preds = recognizer.predict_proba(vec)[0]
            j = np.argmax(preds)
            proba = preds[j]
            name = le.classes_[j]

            if name in authorized_users:
                authentication_result = "Authenticated"  # User is authorized
                # Delay the authenticated function by 10 seconds
                root.after(1000, authenticated)

            text = f"{name}: {proba * 100:.2f}% - {authentication_result}"
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
            cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)
    photo = ImageTk.PhotoImage(image=frame)
    label.config(image=photo)
    label.image = photo

    root.after(int(0.01 * 100), update_frame)  # Update every 10 milliseconds


# Call the update_frame function to start displaying the video stream
update_frame()


# Function to quit the application
def quit_app():
    vs.stop()
    root.quit()


# Create a Quit button to exit the application
quit_button = tk.Button(root, text="Quit", command=quit_app)
quit_button.pack()

# Handle window close button
root.protocol("WM_DELETE_WINDOW", quit_app)

root.mainloop()
