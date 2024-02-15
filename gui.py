import tkinter as tk
from tkinter import ttk, messagebox
from auth import *

def create_main_window():
    """Initialize and return the main application window."""
    root = tk.Tk()
    root.title("Aplikacja")
    root.geometry("800x600")  # Adjust the size as needed
    return root

def create_menu(root):
    """Create and add a menu to the main window."""
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menu_bar)

def create_login_frame(root):
    """Create and add the login frame to the main window."""
    login_frame = ttk.Frame(root, padding="10")
    login_frame.pack(fill='both', expand=True)

    # Add widgets to login_frame
    ttk.Label(login_frame, text="Username:").pack()
    username_entry = ttk.Entry(login_frame)
    username_entry.pack()

    ttk.Label(login_frame, text="Password:").pack()
    password_entry = ttk.Entry(login_frame, show="*")
    password_entry.pack()

    ttk.Button(login_frame, text="Login", command=lambda: login(username_entry.get(), password_entry.get(),root)).pack()

    return login_frame

def login(username, password,root):
    print(1)
    if check_login(username, password):
        #messagebox.showinfo("Login Success", "You have successfully logged in.")
        print(2)
        open_main_interface(root)
    else:

        print(3)
        messagebox.showerror("Login Failed", "The username or password is incorrect")


def create_task_management_frame(root):
    """Create and add the task management frame to the main window."""
    task_mgmt_frame = ttk.Frame(root, padding="10")
    # You can choose to pack this later or swap it with the login frame upon successful login

    # Add widgets to task_mgmt_frame
    # ...

    return task_mgmt_frame

# You can add more functions for different parts of your UI (e.g., reporting interface)

def open_main_interface(root):
    """Open the main application interface."""
    # Here you might want to hide or destroy the login frame
    # and pack the task management frame instead
    try:
        # Assuming you have a function to destroy or hide the login frame
        hide_login_frame()
    except NameError:
        pass  # If there is no login frame, it's the initial call

    # Create and pack the task management frame, for example
    task_mgmt_frame = create_task_management_frame(root)
    task_mgmt_frame.pack(fill='both', expand=True)