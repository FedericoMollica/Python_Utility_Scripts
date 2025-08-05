"""
@author: Federico Mollica

Simple Notepad application using Tkinter
Supports opening, saving, clearing text files, and exiting the app.
"""

import tkinter as tk
from tkinter import Frame, Button, Text, WORD, END, INSERT
from tkinter.filedialog import asksaveasfile, askopenfile

# --------------------------- Library Installation ---------------------------
# Tkinter is included with standard Python installations.
# If tkinter is missing:
# For conda environments, run: conda install tk
# For system-wide installation on Debian/Ubuntu: sudo apt-get install python3-tk
# On Windows and Mac, ensure using the official Python installer that includes tkinter.
# -----------------------------------------------------------------------------

def saveFile():
    """
    Open a save dialog to save the current text content to a file.
    If the operation is cancelled, returns without saving.
    """
    new_file = asksaveasfile(mode='w', filetype=[('Text Files', '.txt')])
    if new_file is None:
        return  # User cancelled save dialog

    # Get all text from the text widget
    text = entry.get(1.0, END)
    new_file.write(text)
    new_file.close()

def openFile():
    """
    Open a file dialog to select a text file and load its content into the text widget.
    """
    file = askopenfile(mode='r', filetype=[('Text Files', '*.txt')])
    if file is not None:
        content = file.read()
        entry.delete(1.0, END)  # Clear existing text before inserting new content
        entry.insert(INSERT, content)
        file.close()

def clearFile():
    """
    Clear all text from the text widget.
    """
    entry.delete(1.0, END)

# --------------------------- GUI Setup ---------------------------------------

# Initialize main window
canvas = tk.Tk()
canvas.geometry("400x600")
canvas.title("Notepad_FM")
canvas.config(bg="white")

# Top frame container for buttons with padding and anchored to northwest
top = Frame(canvas)
top.pack(padx=10, pady=5, anchor='nw')

# Button to open text files
b1 = Button(canvas, text="Open", bg="white", command=openFile)
b1.pack(in_=top, side=tk.LEFT, padx=5)

# Button to save current text to file
b2 = Button(canvas, text="Save", bg="white", command=saveFile)
b2.pack(in_=top, side=tk.LEFT, padx=5)

# Button to clear the text area
b3 = Button(canvas, text="Clear", bg="white", command=clearFile)
b3.pack(in_=top, side=tk.LEFT, padx=5)

# Button to exit the application cleanly
b4 = Button(canvas, text="Exit", bg="white", command=canvas.quit)
b4.pack(in_=top, side=tk.LEFT, padx=5)

# Text widget for the notepad content with word wrapping and custom background/font
entry = Text(canvas, wrap=WORD, bg="#F9DDA4", font=("Poppins", 15))
entry.pack(padx=10, pady=5, expand=True, fill=tk.BOTH)

# Start the Tkinter event loop
canvas.mainloop()
