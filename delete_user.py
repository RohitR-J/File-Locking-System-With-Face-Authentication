import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedStyle
import os
import subprocess
import shutil


def execute_scripts():
    # Function to delete a user from the authorized_user.txt file
    user_to_delete = name_entry.get()  # Get the username from the entry field

    # Check if the username is empty
    if not user_to_delete:
        tk.messagebox.showerror("Error", "Please enter a username")
        return

    # Path to the authorized_user.txt file
    file_path = "authorized_users.txt"

    # Check if the file exists
    if not os.path.exists(file_path):
        tk.messagebox.showerror("Error", "The authorized_user.txt file does not exist.")
        return

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        found = False

        # Create a new list of lines without the user to be deleted
        new_lines = []
        for line in lines:
            if user_to_delete not in line:
                new_lines.append(line)
            else:
                found = True

        if not found:
            tk.messagebox.showerror("Error", f"User '{user_to_delete}' not found")
            return

        # Write the updated lines back to the file
        with open(file_path, "w") as file:
            file.writelines(new_lines)

        # tk.messagebox.showinfo("Success", f"User '{user_to_delete}' has been deleted")

        user_data_folder = f"dataset/{user_to_delete}"

        if os.path.exists(user_data_folder):
            # Delete the user's data folder and its contents
            shutil.rmtree(user_data_folder)
            tk.messagebox.showinfo("Success",
                                   f"User '{user_to_delete}' has been deleted")


    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Execute extract_embeddings.py
    extract_result = subprocess.run(["python", "extract_embeddings.py"])

    # Check if extract_embeddings.py was successful (return code 0)
    if extract_result.returncode == 0:
        # Execute train_model.py
        subprocess.run(["python", "train_model.py"])


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
label = tk.Label(top_frame, text="Delete user", font=("Georgia", 18), fg="white", bg="black")
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

# Add space between the text box and the "Delete" button
space_frame2 = tk.Frame(middle_frame, bg="black")
space_frame2.pack(pady=10)

# Create a ThemedStyle for custom styling
style = ThemedStyle(root)
style.set_theme("adapta")  # Apply the "adapta" theme

# Create a custom style for the Delete button
style.configure("add.TButton", font=("Georgia", 12), foreground="black", background="black")
style.configure("train.TButton", font=("Georgia", 12), foreground="black", background="black")

# Create a modern-style button inside the frame with the custom style
delete_button = ttk.Button(middle_frame, text="Delete", style="add.TButton", command=execute_scripts)
delete_button.pack()


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
