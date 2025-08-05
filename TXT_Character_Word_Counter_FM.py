"""
A simple GUI to load a .txt file, display its contents,
and print character and word counts as a DataFrame in the console.

@author: Federico Mollica

Dependencies:
- pandas (for DataFrame output); install with: pip install pandas
- Tkinter is included in standard Python.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import pandas as pd
import string

def count_stats(text):
    total_characters = len(text)
    characters_no_space = len(text.replace(" ", ""))
    cleaned_text = text.translate(str.maketrans('', '', string.punctuation))
    word_count = len(cleaned_text.split())
    return total_characters, characters_no_space, word_count

def load_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not filepath:
        return
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file:\n{e}")
        return
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, content)

    total_char, char_no_space, word_cnt = count_stats(content)

    # Create DataFrame and print to console
    stats_df = pd.DataFrame({
        "Total Characters": [total_char],
        "Characters (no spaces)": [char_no_space],
        "Word Count": [word_cnt]
    })
    print(stats_df)

root = tk.Tk()
root.title("TXT_Character_Word_Counter_FM")
root.geometry("650x500")
root.config(bg="#F8FAFF")

open_btn = tk.Button(root, text="Open TXT File", font=("Arial", 14), command=load_file, bg="#57a1f8", fg="white", width=18)
open_btn.pack(pady=18)

text_box = ScrolledText(root, font=("Arial", 12), height=25, width=75, wrap="word")
text_box.pack(padx=10, pady=8)

root.mainloop()
