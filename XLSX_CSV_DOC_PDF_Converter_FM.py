#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 18:35:36 2022

@author: Federico Mollica

A Tkinter-based GUI application for:
- .xlsx <-> .csv file conversion using pandas/openpyxl
- .pdf <-> .docx file conversion (pdf2docx: keeps text & images from PDF)
- .doc or .docx to .pdf conversion (using python-docx and reportlab)
"""

import tkinter as tk
from tkinter import Text, Label, Button, INSERT, END, filedialog
import os
import pandas as pd
from pdf2docx import Converter  # Improved: handles images!
from docx import Document
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import A4
import docx2txt

# --------------------------- Library Installation -----------------------------
# Tkinter and os are included with standard Python.
# Additional dependencies:
# pip install pandas openpyxl pillow pdf2docx python-docx reportlab docx2txt
# pdf2docx: enables PDF to DOCX conversion with images/styles
# -----------------------------------------------------------------------------

# ------------------------------ Color Palette ---------------------------------
PURPLE = '#3d3d56'
REDDISH = '#563d47'
WHITE = "#FFFFFF"
DEFAULT_FONT_STYLE = ("Arial", 20)
ENTRY_FONT_STYLE = ("Arial", 14)

# ----------------------------- Main Window Setup ------------------------------
root = tk.Tk()
root.geometry("760x320")
root.title("Converter_FM")
root.config(bg=PURPLE)
root.columnconfigure(0, weight=1)
for r in range(5):
    root.rowconfigure(r, weight=1)

container = tk.Frame(root, bg=PURPLE)
container.grid(column=0, row=0, rowspan=5, padx=0, pady=10, sticky="nsew")

for i in range(7):
    container.rowconfigure(i, weight=1)
container.columnconfigure(0, weight=1)
container.columnconfigure(1, weight=1)

title = Label(container, text="File Converter", font=("Arial", 28, "bold"),
              bg=PURPLE, fg=WHITE)
title.grid(row=0, column=0, columnspan=2, pady=(10,5), sticky="n")

body_label = Label(container, text="Input File:", font=ENTRY_FONT_STYLE, bg=PURPLE, fg=WHITE, anchor="e")
body_label.grid(row=1, column=0, sticky="e", padx=(40, 8), pady=4)

body = Text(container, font=ENTRY_FONT_STYLE, height=1, width=45)
body.grid(row=1, column=1, sticky="w", padx=(0, 40), pady=4)

link_label = Label(container, text="Output Path:", font=ENTRY_FONT_STYLE, bg=PURPLE, fg=WHITE, anchor="e")
link_label.grid(row=2, column=0, sticky="e", padx=(40, 8), pady=4)

link = Text(container, font=ENTRY_FONT_STYLE, height=1, width=45)
link.grid(row=2, column=1, sticky="w", padx=(0, 40), pady=4)

btn_frame = tk.Frame(container, bg=PURPLE)
btn_frame.grid(row=3, column=0, columnspan=2, pady=16)

def search_for_file_path():
    """Open file dialog and display selected path."""
    currdir = os.path.dirname(os.path.abspath(__file__))
    tempdir = filedialog.askopenfilename(parent=root, initialdir=currdir, title='Select a file')
    if tempdir:
        body.delete(1.0, END)
        body.insert(INSERT, tempdir)

def clearFile():
    """Clear both input and output text boxes."""
    body.delete(1.0, END)
    link.delete(1.0, END)

def docx_doc_to_pdf(input_path, output_path):
    """
    Convert DOCX or DOC file to PDF.
    Reads text, one paragraph per line, and writes to PDF using reportlab.
    """
    try:
        if input_path.endswith('.doc'):
            temp_txt = docx2txt.process(input_path)
            paragraphs = temp_txt.split('\n')
        else:
            doc = Document(input_path)
            paragraphs = [para.text for para in doc.paragraphs]

        c = pdf_canvas.Canvas(output_path, pagesize=A4)
        width, height = A4
        y = height - 40
        for para in paragraphs:
            while len(para) > 120:
                c.drawString(40, y, para[:120])
                para = para[120:]
                y -= 20
                if y < 40:
                    c.showPage()
                    y = height - 40
            c.drawString(40, y, para)
            y -= 20
            if y < 40:
                c.showPage()
                y = height - 40
        c.save()
        return True, output_path
    except Exception as e:
        return False, str(e)

def pdf_to_docx_with_images(pdf_file, docx_file):
    """
    Convert PDF to DOCX, preserving images and text using pdf2docx.
    """
    try:
        cv = Converter(pdf_file)
        cv.convert(docx_file, start=0, end=None)
        cv.close()
        return True, docx_file
    except Exception as e:
        return False, str(e)

def conversion():
    """
    Converts between xlsx/csv, pdf->docx (with images!), and docx/doc->pdf.
    Shows result or error.
    """
    insert_path = body.get("1.0", 'end-1c').strip()
    link.delete(1.0, END)
    try:
        if insert_path.endswith('.xlsx'):
            new_path = insert_path.replace('.xlsx', '.csv')
            df = pd.read_excel(insert_path, engine='openpyxl')
            df.to_csv(new_path, index=False)
            link.insert(INSERT, new_path)
        elif insert_path.endswith('.csv'):
            new_path = insert_path.replace('.csv', '.xlsx')
            df = pd.read_csv(insert_path)
            df.to_excel(new_path, index=False, engine='openpyxl')
            link.insert(INSERT, new_path)
        elif insert_path.endswith('.pdf'):
            new_path = insert_path.replace('.pdf', '.docx')
            success, msg = pdf_to_docx_with_images(insert_path, new_path)
            if success:
                link.insert(INSERT, new_path)
            else:
                link.insert(INSERT, f"[ERROR: {msg}]")
        elif insert_path.endswith('.docx') or insert_path.endswith('.doc'):
            new_path = (insert_path.rsplit('.', 1)[0]) + '.pdf'
            success, msg = docx_doc_to_pdf(insert_path, new_path)
            if success:
                link.insert(INSERT, new_path)
            else:
                link.insert(INSERT, f"[ERROR: {msg}]")
        else:
            link.insert(INSERT, "[ERROR: Please select a .csv, .xlsx, .pdf, .docx, or .doc file]")
    except Exception as e:
        link.insert(INSERT, f"[ERROR: {e}]")

button_style = {'bg': REDDISH, 'fg': WHITE, 'font': DEFAULT_FONT_STYLE, 'width': 12}

open_btn = Button(btn_frame, text="Open File", command=search_for_file_path, **button_style)
open_btn.pack(side="left", padx=12)
convert_btn = Button(btn_frame, text="Convert", command=conversion, **button_style)
convert_btn.pack(side="left", padx=12)
clear_btn = Button(btn_frame, text="Clear", command=clearFile, **button_style)
clear_btn.pack(side="left", padx=12)


root.mainloop()
