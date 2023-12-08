import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import subprocess
import os


def execute_scripts():
    # Execute extract_embeddings.py
    extract_result = subprocess.run(["python", "extract_embeddings.py"])

    # Check if extract_embeddings.py was successful (return code 0)
    if extract_result.returncode == 0:
        # Execute train_model.py
        subprocess.run(["python", "train_model.py"])


# Function to add a user to the authorized users list
def add_user():
    user_name = name_entry.get()
    if user_name.strip() == "":
        add_label.config(text="Name is required", fg="red")
    else:
        with open("authorized_users.txt", "a") as file:
            file.write(user_name + "\n")
        add_label.config(text="Click to recognize the face", fg="white")
        subprocess.run(["python", "image_clicker.py", user_name])


root = tk.Tk()
root.title("Admin")

# Set the window dimensions
window_width = 600
window_height = 400
root.geometry(f"{window_width}x{window_height}")

# Create a Canvas widget for the background image
bg_canvas = tk.Canvas(root, width=window_width, height=window_height)
bg_canvas.pack()

# Load the background image for the entire window
bg_image = tk.PhotoImage(file="C:/Users/Rohit/Desktop/Rohit/Rohit/facelock_tester/app/images/login2.png")

# Place the background image on the Canvas
bg_canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)

# Create a frame for the top-center with increased size
top_frame = tk.Frame(root, width=500, height=50, bg="black")
top_frame.place(relx=0.5, rely=0.1, anchor="n")

# Create a label with text inside the heading frame
label = tk.Label(top_frame, text="Add New User Panel", font=("Georgia", 18), fg="white", bg="black")
label.pack()

# Create a frame in the middle with an increased size
middle_frame = tk.Frame(root, width=500, height=300, bg="black")
middle_frame.place(relx=0.5, rely=0.5, anchor="center")

# Add space between the label and the button
space_frame = tk.Frame(middle_frame, bg="black")
space_frame.pack(pady=8)

# Create a label for "Enter name:"
name_label = tk.Label(middle_frame, text="Enter name:", font=("Helvetica", 12), fg="white", bg="black", anchor="w")
name_label.pack()

# Create a text box for entering a name
name_entry = tk.Entry(middle_frame, font=("Helvetica", 12))
name_entry.pack()

# Add space between the text box and the "ADD" button
space_frame2 = tk.Frame(middle_frame, bg="black")
space_frame2.pack(pady=10)

# Create a ThemedStyle for custom styling
style = ThemedStyle(root)
style.set_theme("adapta")  # Apply the "adapta" theme

# Create a custom style for the Add button
style.configure("add.TButton", font=("Georgia", 12), foreground="black", background="black")
style.configure("train.TButton", font=("Georgia", 12), foreground="black", background="black")

# Create a modern-style button inside the frame with the custom style
add_button = ttk.Button(middle_frame, text="ADD", style="add.TButton", command=add_user)
add_button.pack()

# Create a label below the Add button
add_label = tk.Label(middle_frame, text="Click to recognize the face", font=("Helvetica", 8), fg="white", bg="black")
add_label.pack()

# Add space between the buttons
space_frame3 = tk.Frame(middle_frame, bg="black")
space_frame3.pack(pady=8)

# Create a modern-style button inside the frame with the custom style
train_button = ttk.Button(middle_frame, text="Save", style="train.TButton", command=execute_scripts)
train_button.pack()


def quit():
    root.destroy()


space_frame4 = tk.Frame(middle_frame, bg="black")
space_frame4.pack(pady=10)


def quit():
    root.destroy()


style.configure("quit.TButton", font=("Georgia", 12), foreground="black", background="black")

quit_button = ttk.Button(middle_frame, text="Quit", style="quit.TButton", command=quit)
quit_button.pack()

root.mainloop()
