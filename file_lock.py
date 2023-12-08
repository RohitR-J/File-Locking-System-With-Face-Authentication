import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from cryptography.fernet import Fernet
import os
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle
import subprocess


def open_add_user():
    # Execute add_user.py using subprocess
    subprocess.run(["python", "add_user.py"])


def open_delete_user():
    # Execute delete_user.py using subprocess
    subprocess.run(["python", "delete_user.py"])


class FaceLock:
    def __init__(self, root):
        self.root = root
        self.root.title("File Locking System")
        self.root.geometry("600x400")
        self.keys = {}

        # Dictionary to store keys for each file
        # Load and set the background image

        background_image = Image.open(
            "C:/Users/Rohit/Desktop/Rohit/Rohit/facelock - Copy/images/lock3.png")  # Replace with your image file
        self.background_image = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

        # Create a button for logout
        logout_button = tk.Button(self.root, text="Logout", font=("Georgia", 12), command=self.logout)
        logout_button.place(relx=0.95, rely=0.05, anchor="ne")

        style = ThemedStyle(self.root)  # Create a ThemedStyle object
        style.set_theme("adapta")  # Set the theme to "adapta"

        # Create a frame at the top center with a heading
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, pady=20)  # Add some padding

        heading_label = tk.Label(top_frame, text="File Locking", font=("Georgia", 18), foreground="white",
                                 background="black")
        heading_label.pack()

        # Create a frame in the center
        center_frame = tk.Frame(self.root)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.create_gui(center_frame)

    def save_keys(self, filename="keys.txt"):
        with open(filename, 'w') as key_file:
            for file_name, key in self.keys.items():
                key_file.write(f"{file_name}::{key.decode()}\n")

    def load_keys(self, filename="keys.txt"):
        if os.path.exists(filename):
            with open(filename, 'r') as key_file:
                lines = key_file.readlines()
                for line in lines:
                    file_name, key = line.strip().split("::")
                    self.keys[file_name] = key.encode()

    def encrypt_file(self):
        try:
            key = Fernet.generate_key()
            cipher_suite = Fernet(key)
            file_path = filedialog.askopenfilename()

            with open(file_path, 'rb') as file:
                file_data = file.read()

            encrypted_data = cipher_suite.encrypt(file_data)

            with open(file_path, 'wb') as file:
                file.write(encrypted_data)

            key_folder = "C:/Users/Rohit/Desktop/Rohit/Rohit/facelock - Copy/key"  # Specify the folder path
            os.makedirs(key_folder, exist_ok=True)
            file_name = os.path.basename(file_path)
            key_file_path = os.path.join(key_folder, f'{file_name}_key.key')

            with open(key_file_path, 'wb') as key_file:
                key_file.write(key)

            self.keys[file_name] = key  # Store the key in the dictionary
            self.save_keys()  # Save the keys to a file

            messagebox.showinfo(title="File Encryption", message="The file has been encrypted successfully.")
        except Exception as e:
            messagebox.showerror(title="File Encryption Error", message=e)

    def decrypt_file(self):
        try:
            file_path = filedialog.askopenfilename()
            file_name = os.path.basename(file_path)

            if file_name not in self.keys:
                messagebox.showerror(title="File Decryption Error", message="No key found for this file.")
                return

            key = self.keys[file_name]
            cipher_suite = Fernet(key)

            with open(file_path, 'rb') as file:
                encrypted_data = file.read()

            decrypted_data = cipher_suite.decrypt(encrypted_data)

            with open(file_path, 'wb') as file:
                file.write(decrypted_data)

            messagebox.showinfo(title="File Decryption", message="The file has been decrypted successfully.")
        except Exception as e:
            messagebox.showerror(title="File Decryption Error", message=e)

    def logout(self):
        # Perform logout actions here
        # For example, you can destroy the current window
        self.root.destroy()

    def create_gui(self, frame):
        # Use ttk.Buttons to apply the theme to buttons
        encrypt_button = ttk.Button(frame, text="Encrypt File", command=self.encrypt_file)
        decrypt_button = ttk.Button(frame, text="Decrypt File", command=self.decrypt_file)

        encrypt_button.pack()
        decrypt_button.pack()

        # Create a frame in the bottom-right corner
        bottom_frame = tk.Frame(root, width=500, height=50, bg="black")
        bottom_frame.place(relx=0.95, rely=0.95, anchor="se")

        # Create a button inside the bottom frame for adding a new user
        add_user_button = tk.Button(bottom_frame, text="Add new user", font=("Georgia", 12), fg="white", bg="black",
                                    command=open_add_user)
        add_user_button.pack()

        space_frame = tk.Frame(bottom_frame, bg="black")
        space_frame.pack(pady=4)

        # Create a button inside the bottom frame for deleting a user
        delete_user_button = tk.Button(bottom_frame, text="Delete user", font=("Georgia", 12), fg="white", bg="black",
                                       command=open_delete_user)
        delete_user_button.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceLock(root)
    app.load_keys()  # Load keys from a file at the start of the program
    root.mainloop()
