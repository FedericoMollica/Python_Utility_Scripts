#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 19:12:13 2022
Author: Federico Mollica

A simple calculator application built with Tkinter.
Features basic arithmetic operations, square, square root,
and keyboard input support.

Dependencies:
- Python standard library (tkinter)

Library installation:

To use tkinter, it usually comes pre-installed with Python.
If tkinter is not installed:
- On conda environments:
    conda install tk
- On pip/virtualenv environments, install python-tk (specific to OS):
    For Debian/Ubuntu: sudo apt-get install python3-tk
    For Windows/Mac, tkinter is bundled with standard Python installer.

Run the script:
$ python calculator.py
"""

import tkinter as tk  # Import tkinter for GUI development


# ------------------ Constants for Styles and Colors -------------------

LARGE_FONT_STYLE = ("Arial", 40, "bold")     # Font for main display numbers
SMALL_FONT_STYLE = ("Arial", 16)             # Font for the total (previous entries)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")    # Font for digit buttons
DEFAULT_FONT_STYLE = ("Arial", 20)           # Font for operator and special buttons

# Color palette used for backgrounds and text
OFF_WHITE = "#F8FAFF"    # Light background for buttons
WHITE = "#FFFFFF"        # White background for digit buttons
LIGHT_BLUE = "#CCEDFF"   # Equals button background
LIGHT_GRAY = "#F5F5F5"   # Display background
LABEL_COLOR = "#25265E"  # Text color for labels and buttons


class Calculator:
    """
    Calculator GUI and logic implemented with tkinter.
    Supports basic arithmetic operations, square, and square root operations.
    Enables input via buttons and keyboard.
    """

    def __init__(self):
        """Initialize the main window, UI components and bind events."""
        self.window = tk.Tk()
        self.window.geometry("375x667")  # Set fixed window size for consistent layout
        self.window.resizable(0, 0)      # Disable resizing to maintain design integrity
        self.window.title("Calculator_FM")

        # Expressions used for calculation and display
        self.total_expression = ""       # Holds the entire expression as string
        self.current_expression = ""     # Holds the current number or operator

        self.display_frame = self.create_display_frame()

        # Labels to show current and total expressions
        self.total_label, self.label = self.create_display_labels()

        # Positions for digit buttons (row, column)
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }

        # Supported operations and their displayed symbols
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        self.buttons_frame = self.create_buttons_frame()

        # Configure grid rows and columns to be expandable equally
        self.buttons_frame.rowconfigure(0, weight=1)
        for i in range(1, 5):
            self.buttons_frame.rowconfigure(i, weight=1)
            self.buttons_frame.columnconfigure(i, weight=1)

        # Create all buttons in the UI
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()

        # Bind keyboard input to functions
        self.bind_keys()

    def bind_keys(self):
        """Bind keyboard keys to calculator functions."""
        self.window.bind("<Return>", lambda event: self.evaluate())   # Enter key to calculate
        self.window.bind("<Delete>", lambda event: self.clear())      # Delete key clears all (like 'C' button)
        self.window.bind("<BackSpace>", lambda event: self.delete())  # Backspace deletes last char

        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_display_frame(self):
        """Create and return the frame that contains the calculator's display."""
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def create_display_labels(self):
        """
        Create and return two labels:
        - total_label: to display the full expression in smaller font
        - label: to display the current input in larger font
        """
        total_label = tk.Label(
            self.display_frame, text=self.total_expression, anchor=tk.E,
            bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE
        )
        total_label.pack(expand=True, fill='both')

        label = tk.Label(
            self.display_frame, text=self.current_expression, anchor=tk.E,
            bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE
        )
        label.pack(expand=True, fill='both')

        return total_label, label

    def add_to_expression(self, value):
        """
        Add a digit or decimal point to the current expression
        and update the display label.
        """
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        """Create digit buttons (0-9 and decimal point) and add to buttons frame."""
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame,
                               text=str(digit),
                               bg=WHITE,
                               fg=LABEL_COLOR,
                               font=DIGITS_FONT_STYLE,
                               borderwidth=0,
                               command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        """
        Append the current expression and operator to the total expression,
        clear current expression, and update display.
        """
        # Do not allow operator if expression is empty (to prevent errors)
        if self.current_expression == "" and self.total_expression == "":
            return
        # Replace last operator if current is empty and last expression ends with operator
        if self.current_expression == "" and self.total_expression and self.total_expression[-1] in self.operations:
            self.total_expression = self.total_expression[:-1] + operator
        else:
            self.total_expression += self.current_expression + operator
            self.current_expression = ""

        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        """Create operator buttons (+, -, *, /) and add to buttons frame."""
        for i, (operator, symbol) in enumerate(self.operations.items()):
            button = tk.Button(self.buttons_frame,
                               text=symbol,
                               bg=OFF_WHITE,
                               fg=LABEL_COLOR,
                               font=DEFAULT_FONT_STYLE,
                               borderwidth=0,
                               command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)

    def clear(self):
        """
        Clear the current and total expressions and update display.
        """
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        """Create the Clear button (C) and add to buttons frame."""
        button = tk.Button(self.buttons_frame,
                           text="C",
                           bg=OFF_WHITE,
                           fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE,
                           borderwidth=0,
                           command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def delete(self):
        """
        Delete the last character from the current expression and update display.
        """
        self.current_expression = self.current_expression[:-1]
        self.update_label()

    def square(self):
        """Calculate the square of the current expression and update display."""
        try:
            result = eval(f"({self.current_expression})**2")
            self.current_expression = str(result)
        except Exception:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_square_button(self):
        """Create the square button (x²) and add to buttons frame."""
        button = tk.Button(self.buttons_frame,
                           text="x\u00b2",
                           bg=OFF_WHITE,
                           fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE,
                           borderwidth=0,
                           command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        """Calculate the square root of the current expression and update display."""
        try:
            result = eval(f"({self.current_expression})**0.5")
            self.current_expression = str(result)
        except Exception:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_sqrt_button(self):
        """Create the square root button (√x) and add to buttons frame."""
        button = tk.Button(self.buttons_frame,
                           text="\u221ax",
                           bg=OFF_WHITE,
                           fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE,
                           borderwidth=0,
                           command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        """
        Evaluate the total expression appended with the current expression.
        Update the display with the result or show 'Error' on failure.
        """
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            # Evaluate the math expression safely
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        """Create the equals button (=) and add to buttons frame."""
        button = tk.Button(self.buttons_frame,
                           text="=",
                           bg=LIGHT_BLUE,
                           fg=LABEL_COLOR,
                           font=DEFAULT_FONT_STYLE,
                           borderwidth=0,
                           command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_special_buttons(self):
        """
        Create all special function buttons:
        Clear (C), square (x²), square root (√x), Equals (=).
        """
        self.create_clear_button()
        self.create_square_button()
        self.create_sqrt_button()
        self.create_equals_button()

    def create_buttons_frame(self):
        """Create and return the frame that contains the buttons."""
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        """
        Update the total expression label with pretty symbols instead of
        Python operators for better readability.
        """
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        """
        Update the current expression label.
        Limit display length to maximum 11 characters.
        """
        self.label.config(text=self.current_expression[:11])

    def run(self):
        """Run the Tkinter main event loop to start the application."""
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
