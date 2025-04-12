# Author: Haoji Zang
# Date: 04/03/2025
# Description: Nutrition UI with total calorie display.

import tkinter as tk
from tkinter import messagebox
import pandas as pd
from nutrition import NutritionTracker

# Defines a class named NutritionUI
class NutritionUI:
    def __init__(self, root, username):
        self.username = username # Current logged-in user's name
        self.tracker = NutritionTracker()

        self.root = tk.Toplevel(root) # A new top-level window
        self.root.title("Nutrition Tracker")
        self.root.geometry("420x500")

        food_df = pd.read_csv("reference/Food and Calories.csv") # Loaded from "reference/Food and Calories.csv"
        self.food_list = food_df["Food"].tolist() # A list of food names

        self.build_ui()
        self.refresh_summary()

    def build_ui(self):
        tk.Label(self.root, text="Enter food name:").pack()
        self.food_entry = tk.Entry(self.root)
        self.food_entry.pack(pady=3)

        tk.Label(self.root, text="Enter weight in grams:").pack()
        self.grams_entry = tk.Entry(self.root)
        self.grams_entry.pack(pady=3)

        tk.Button(self.root, text="Save Entry", command=self.save_entry).pack(pady=10)
        tk.Button(self.root, text="Show Available Food List", command=self.show_food_list).pack(pady=5)

        self.total_label = tk.Label(self.root, text="")
        self.total_label.pack(pady=5)

        tk.Button(self.root, text="Clear Today's Records", command=self.clear_today_data).pack(pady=5)
        tk.Button(self.root, text="Export Today's Records", command=self.export_today).pack(pady=5)

        tk.Button(self.root, text="Show Weekly Intake Trend").pack(pady=5)

    def save_entry(self):
        """
        Save a food record entered by the user to the CSV file.
        """
        try:
            # Get input values from the user
            food = self.food_entry.get()
            grams = float(self.grams_entry.get())

            # Validate inputs
            if grams <= 0 or not food.strip():
                raise ValueError

            # Save entry
            self.tracker.add_food_entry(self.username, food.strip(), grams)

            # Show success message
            messagebox.showinfo("Success", f"Saved: {food.strip()} - {grams}g")

            # Clear input fields after saving
            self.grams_entry.delete(0, tk.END)
            self.food_entry.delete(0, tk.END)

            # Update today's summary display
            self.refresh_summary()

        except ValueError:
            # Show error if input is invalid
            messagebox.showerror("Error", "Please enter a valid food name and a positive weight.")

    def refresh_summary(self):
        """
        Refresh and display today's total calorie and nutrient intake.
        """
        total = self.tracker.summarize_daily_nutrition(self.username)
        self.total_label.config(text=f"Total calories consumed today: {total['calories']} kcal")

    def clear_today_data(self):
        """
        Clear all nutrition records for today and refresh display.
        """
        self.tracker.clear_today_nutrition(self.username)
        messagebox.showinfo("Cleared", "Today's nutrition records have been cleared.")
        self.refresh_summary()

    def export_today(self):
        """
        Show all food entries for today in a popup window.
        """
        records = self.tracker.get_today_entries(self.username)

        # No records case
        if not records:
            messagebox.showinfo("Notice", "No records found for today.")
            return

        # Construct a string with all entries for today
        text = "Today's Nutrition Details:\n"
        for row in records:
            text += f"{row[1]} - {row[2]}g - {row[3]} kcal\n"

        # Show the results in a message box
        messagebox.showinfo("Today's Records", text)

    def show_food_list(self):
        """
        Display a scrollable list of all available food names.
        """
        # Create a new popup window
        win = tk.Toplevel(self.root)
        win.title("Available Food List")
        win.geometry("300x400")

        # Create scrollbar on the right
        scrollbar = tk.Scrollbar(win)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create listbox and attach scrollbar
        listbox = tk.Listbox(win, yscrollcommand=scrollbar.set)
        for food in sorted(self.food_list):
            listbox.insert(tk.END, food)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
