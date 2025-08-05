"""
@author: Federico Mollica

A clean, centered login GUI using Tkinter.
"""

import tkinter as tk
from tkinter import messagebox

# --------------------------- Library Installation ---------------------------
# Tkinter is included with standard Python installations.
# If tkinter is missing:
# For conda environments, run: conda install tk
# For system-wide installation on Debian/Ubuntu: sudo apt-get install python3-tk
# On Windows and Mac, ensure using the official Python installer that includes tkinter.
# -----------------------------------------------------------------------------

# Main application window setup
root = tk.Tk()
root.title('Login_GUI_FM')
root.geometry('500x500+300+200')      # Window size 500x500 pixels, positioned on screen
root.configure(bg='#fff')             # White background for clean look
root.resizable(False, False)          # Disable window resizing for fixed layout

# Hardcoded credentials for demonstration purposes
your_username = 'admin'
your_password = 'admin'

# Centered frame setup inside main window with blue border highlight
frame = tk.Frame(
    root,
    width=350,
    height=350,
    bg='white',
    highlightbackground='#57a1f8',
    highlightcolor='#57a1f8',
    highlightthickness=2
)
# Place frame at center of main window
frame.place(relx=0.5, rely=0.5, anchor='center')

# Heading label for the login form
heading = tk.Label(
    frame,
    text='Sign In',
    fg='#57a1f8',        # Blue color matching highlight
    bg='white',
    font=('Arial', 32, 'bold')
)
heading.pack(pady=(24, 16))           # Top and bottom padding for spacing

# ---------------------------------- Placeholder Logic ----------------------------------

def on_enter_user(event):
    """Clear placeholder text from username field on focus, set text color."""
    if user_entry.get() == 'Username':
        user_entry.delete(0, 'end')
        user_entry.config(fg='black')

def on_leave_user(event):
    """Restore placeholder text in username field if empty on focus out."""
    if user_entry.get() == '':
        user_entry.insert(0, 'Username')
        user_entry.config(fg='grey')

def on_enter_pass(event):
    """Clear placeholder text and enable masking for password field on focus."""
    if pass_entry.get() == 'Password':
        pass_entry.delete(0, 'end')
        pass_entry.config(show='*', fg='black')    # Mask password input

def on_leave_pass(event):
    """Restore placeholder text and disable masking if password field empty."""
    if pass_entry.get() == '':
        pass_entry.config(show='', fg='grey')
        pass_entry.insert(0, 'Password')

# ------------------------------ Entry Fields -----------------------------------

# Username input field with grey placeholder text initially
user_entry = tk.Entry(
    frame,
    width=24,
    fg='grey',
    borderwidth=2,
    relief='groove',
    bg='white',
    font=('Arial', 16)
)
user_entry.pack(pady=12)
user_entry.insert(0, 'Username')                 # Set placeholder
user_entry.bind('<FocusIn>', on_enter_user)      # Bind focus in/out events for placeholder behavior
user_entry.bind('<FocusOut>', on_leave_user)

# Password input field with grey placeholder text and masking on focus
pass_entry = tk.Entry(
    frame,
    width=24,
    fg='grey',
    borderwidth=2,
    relief='groove',
    bg='white',
    font=('Arial', 16)
)
pass_entry.pack(pady=12)
pass_entry.insert(0, 'Password')                 # Set placeholder
pass_entry.bind('<FocusIn>', on_enter_pass)      # Bind focus in/out events for placeholder behavior
pass_entry.bind('<FocusOut>', on_leave_pass)

# ----------------------------- Sign In Logic ------------------------------------

def sign_in():
    """Validate the input credentials and show a greeting window or error message."""
    username = user_entry.get()
    password = pass_entry.get()
    if username == your_username and password == your_password:
        # Open new window on successful login
        screen = tk.Toplevel(root)
        screen.title('Welcome')
        screen.geometry('350x200+300+200')
        screen.configure(bg='white')
        msg = tk.Label(
            screen,
            text='Hello Everyone!',
            bg='white',
            fg='#57a1f8',
            font=('Arial', 28, 'bold')
        )
        msg.pack(expand=True)
    else:
        # Show error message box on invalid credentials
        messagebox.showerror('Invalid', 'Invalid username or password')

# ----------------------------- Buttons ------------------------------------------

# Sign In button styled to match theme and placed with padding
sign_in_btn = tk.Button(
    frame,
    text='Sign In',
    bg='#57a1f8',       # Theme blue background
    fg='white',         # White text
    font=('Arial', 16, 'bold'),
    width=18,
    border=0,
    pady=6,
    command=sign_in     # Call sign_in function when clicked
)
sign_in_btn.pack(pady=(20, 10))

# Informational label below button
info_label = tk.Label(
    frame,
    text="Don't have an account?",
    fg='black',
    bg='white',
    font=('Arial', 12)
)
info_label.pack()

# Sign Up button styled as a text link (no real command attached)
sign_up_btn = tk.Button(
    frame,
    text='Sign Up',
    border=0,
    bg='white',
    fg='#57a1f8',
    font=('Arial', 12, 'underline')
)
sign_up_btn.pack(pady=(0, 8))

# --------------------------------- Run Application ---------------------------------

root.mainloop()
