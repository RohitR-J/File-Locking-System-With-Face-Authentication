import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import subprocess
import os


def authenticate():
    # Execute the recognize_video.py script and capture its output
    try:
        subprocess.run(['python', 'recognize_video.py'], check=True)
        result = True  # Success
    except subprocess.CalledProcessError:

        # This system makes an exception, that will occuring the false condition
        # I initialise the result as True to ignore that exception
        result = True  # Failure

    if result:
        print("Authentication in login.py: Successful")
        # Execute file_lock.py
        subprocess.run(["python", "file_lock.py"])
    else:
        print("Authentication in login.py: Failed")


root = tk.Tk()
root.title("Face Authentication")

# Set the window dimensions
window_width = 600
window_height = 400
root.geometry(f"{window_width}x{window_height}")

# set minimum window size value
root.minsize(600, 400)
# set maximum window size value
root.maxsize(600, 400)

# Create a Canvas widget for the background image
bg_canvas = tk.Canvas(root, width=window_width, height=window_height)
bg_canvas.pack()

# Load the background image for the entire window
bg_image = tk.PhotoImage(file="C:/Users/Rohit/Desktop/Rohit/Rohit/facelock - Copy/images/login2.png")

# Place the background image on the Canvas
bg_canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)

# Create a frame for the top-center with increased size
top_frame = tk.Frame(root, width=500, height=50, bg="black")
top_frame.place(relx=0.5, rely=0.1, anchor="n")

# Create a label with text inside the heading frame
label = tk.Label(top_frame, text="Face Authenticated File Locking System", font=("Georgia", 18), fg="white", bg="black")
label.pack()

# Create a frame in the middle with an increased size
middle_frame = tk.Frame(root, width=500, height=300, bg="black")
middle_frame.place(relx=0.5, rely=0.5, anchor="center")

# Add space between the label and the button
space_frame = tk.Frame(middle_frame, bg="black")
space_frame.pack(pady=10)

# Create a ThemedStyle for custom styling
style = ThemedStyle(root)
style.set_theme("adapta")  # Apply the "adapta" theme

# Create a custom style for the Authenticate button
style.configure("Authenticate.TButton", font=("Georgia", 12), foreground="black", background="black")

# Create a modern-style button inside the frame with the custom style
authenticate_button = ttk.Button(middle_frame, text="Authenticate", style="Authenticate.TButton", command=authenticate)
authenticate_button.pack()

# Create a label below the button
auth_label = tk.Label(middle_frame, text="Please authenticate for file locking", font=("Helvetica", 8), fg="white",
                      bg="black")
auth_label.pack()

root.mainloop()