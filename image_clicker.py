# image_clicker.py
import cv2
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
import threading
import time
from tkinter import messagebox
import sys
import os  # Import the os module

# Initialize the camera
cam = cv2.VideoCapture(0)  # Use the default camera (0)

user_name = sys.argv[1] if len(sys.argv) > 1 else None


def update_camera_view():
    result, frame = cam.read()
    if result:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(Image.fromarray(frame))
        camera_label.config(image=photo)
        camera_label.image = photo
        camera_label.after(10, update_camera_view)


def capture_images():
    for count in range(10):
        result, image = cam.read()
        if result:
            if user_name:
                user_folder = os.path.join("dataset", user_name)
                os.makedirs(user_folder, exist_ok=True)
                image_name = os.path.join(user_folder, f"{count}.png")
                cv2.imwrite(image_name, image)
                print(f"Image {count + 1} captured and saved as {image_name}")
                if count < 9:
                    messagebox.showinfo("Capture Info", "Change your face angle")
                    time.sleep(1)
                else:
                    messagebox.showinfo("Success", "New user added successfully.")
                    app.quit()  # Close the image capture window
        else:
            print("No image detected. Please try again.")


def start_capture():
    capture_button.config(state="disabled")
    threading.Thread(target=capture_images).start()


app = tk.Tk()
app.title("Automatic Image Capture")
app.geometry("600x530")

# set minimum window size value
app.minsize(600, 530)
# set maximum window size value
app.maxsize(600, 530)

# Create a label to display the camera view
camera_label = tk.Label(app)
camera_label.pack()

# Apply the "adapta" theme
style = ThemedStyle(app)
style.set_theme("adapta")

# Create the "Start" button with ttk style and configure the font
style.configure("TButton", font=("Georgia", 12))
capture_button = ttk.Button(app, text="Start", command=start_capture, style="TButton")
capture_button.pack()

# Start updating the camera view
update_camera_view()

app.mainloop()
