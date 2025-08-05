#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 18:35:36 2022

@author: Federico Mollica

A Tkinter-based GUI application for converting between .xlsx and .csv files.
"""

import tkinter as tk
from tkinter import Text, Label, Button, INSERT, END
from tkinter import filedialog
import pandas as pd

# --------------------- Library Installation Instructions ----------------------
# Tkinter and os are included with standard Python.
# Pandas for spreadsheet support:       pip install pandas       or   conda install pandas
# openpyxl (required for pandas .xlsx): pip install openpyxl     or   conda install openpyxl


# ------------------------------ Color Palette ---------------------------------
PURPLE = '#3d3d56'
REDDISH = '#563d47'
WHITE = "#FFFFFF"
DEFAULT_FONT_STYLE = ("Arial", 16)
ENTRY_FONT = ("Arial", 13)

# ----------------------------- Main Window Setup ------------------------------
root = tk.Tk()
root.geometry("650x300")
root.title("CSV_XLSX_Converter_FM")
root.configure(bg=PURPLE)

# Grid configuration for responsiveness and centering
root.columnconfigure(0, weight=1)
for r in range(5):
    root.rowconfigure(r, weight=1)

# ------------------------------ Filepath Entries ------------------------------

# Entry for the file to convert
input_label = Label(root, text="Input File", font=DEFAULT_FONT_STYLE, bg=PURPLE, fg=WHITE)
input_label.grid(row=1, column=0, sticky="e", padx=(80, 10), pady=(5, 0))

body = Text(root, font=ENTRY_FONT, height=1, width=42)
body.grid(row=1, column=1, sticky="w", padx=(0, 60), pady=(5, 0))

# Entry for the output file/resulting path
output_label = Label(root, text="Output Path", font=DEFAULT_FONT_STYLE, bg=PURPLE, fg=WHITE)
output_label.grid(row=3, column=0, sticky="e", padx=(80, 10), pady=(5, 0))

link = Text(root, font=ENTRY_FONT, height=1, width=42)
link.grid(row=3, column=1, sticky="w", padx=(0, 60), pady=(5, 0))

# ------------------------------ Functions -------------------------------------

def search_for_file_path():
    """Open file dialog, select a file and display its path."""
    tempdir = filedialog.askopenfilename(parent=root, title='Select a file')
    if tempdir:
        body.delete(1.0, END)
        body.insert(INSERT, tempdir)

def clearFile():
    """Clear both input and output boxes."""
    body.delete(1.0, END)
    link.delete(1.0, END)

def conversion():
    """
    Convert .xlsx to .csv or .csv to .xlsx.
    Show new path or error.
    """
    insert_path = body.get("1.0", 'end-1c').strip()
    link.delete(1.0, END)
    try:
        if insert_path.endswith('.xlsx'):
            new_path = insert_path.replace('.xlsx', '.csv')
            pd.read_excel(insert_path).to_csv(new_path, index=False)
            link.insert(INSERT, new_path)
        elif insert_path.endswith('.csv'):
            new_path = insert_path.replace('.csv', '.xlsx')
            pd.read_csv(insert_path).to_excel(new_path, index=False)
            link.insert(INSERT, new_path)
        else:
            link.insert(INSERT, "[ERROR: Please select a .csv or .xlsx file]")
    except Exception as e:
        link.insert(INSERT, f"[ERROR: {e}]")

# ------------------------------ Button Row ------------------------------------

button_frame = tk.Frame(root, bg=PURPLE)
button_frame.grid(row=0, column=0, columnspan=2, pady=(35,15))

open_btn = Button(button_frame, text="Open File", bg=REDDISH, fg=WHITE, font=DEFAULT_FONT_STYLE, width=12, command=search_for_file_path)
open_btn.pack(side="left", padx=8)

convert_btn = Button(button_frame, text="Convert", bg=REDDISH, fg=WHITE, font=DEFAULT_FONT_STYLE, width=12, command=conversion)
convert_btn.pack(side="left", padx=8)

clear_btn = Button(button_frame, text="Clear", bg=REDDISH, fg=WHITE, font=DEFAULT_FONT_STYLE, width=12, command=clearFile)
clear_btn.pack(side="left", padx=8)

# ------------------------------ Run App! --------------------------------------
root.mainloop()
