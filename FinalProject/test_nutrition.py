# test_nutrition_ui.py

import tkinter as tk
from nutrition_ui import NutritionUI

def main():
    # Use a test username (won't affect actual user data)
    username = "test_user"

    # Create the main Tkinter root window but keep it hidden
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Create the Nutrition UI as a child window
    NutritionUI(root, username)

    # Start the Tkinter event loop to keep the window active
