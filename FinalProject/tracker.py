# tracker.py - only tracker_screen updated

import tkinter as tk
from tkinter import messagebox
import os
import csv
from datetime import datetime, timedelta
# from nutrition_ui import nutrition_screen
# from exercise_ui import exercise_screen
# from visualize import show_weekly_plot

# from utils.helpers import today_str, get_user_data_path, ensure_data_file

def tracker_screen(root, username):
    for widget in root.winfo_children():
        widget.destroy()

    ensure_data_file(username)

    frame = tk.Frame(root, padx=30, pady=20)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text=f"Hello, {username}!", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

    # Input fields
    tk.Label(frame, text="Calories In (eaten):", font=("Helvetica", 12)).grid(row=1, column=0, sticky='e', pady=5)
    in_entry = tk.Entry(frame, font=("Helvetica", 12), width=20)
    in_entry.grid(row=1, column=1, pady=5)

    tk.Label(frame, text="Calories Out (burned):", font=("Helvetica", 12)).grid(row=2, column=0, sticky='e', pady=5)
    out_entry = tk.Entry(frame, font=("Helvetica", 12), width=20)
    out_entry.grid(row=2, column=1, pady=5)

    tk.Label(frame, text="Daily Goal:", font=("Helvetica", 12)).grid(row=3, column=0, sticky='e', pady=5)
    goal_entry = tk.Entry(frame, font=("Helvetica", 12), width=20)
    goal_entry.grid(row=3, column=1, pady=5)

    def save():
        try:
            in_cal = int(in_entry.get())
            out_cal = int(out_entry.get())
            goal = int(goal_entry.get())
            save_entry(username, in_cal, out_cal, goal)
            messagebox.showinfo("Saved", "Today's data saved.")
        except ValueError:
            messagebox.showerror("Error", "Please enter numeric values.")

    def show_summary():
        data = summarize_today(username)
        if data:
            summary = f"Calories In: {data['in_cal']}\nCalories Out: {data['out_cal']}\nGoal: {data['goal']}"
            messagebox.showinfo("Today’s Summary", summary)
        else:
            messagebox.showinfo("No Data", "No entry for today yet.")

    # Buttons
    tk.Button(frame, text="Save Data", font=("Helvetica", 11), bg="#4CAF50", fg="white", width=15, command=save).grid(row=4, column=0, pady=15)
    tk.Button(frame, text="View Summary", font=("Helvetica", 11), bg="#607D8B", fg="white", width=15, command=show_summary).grid(row=4, column=1, pady=15)

    # tk.Button(frame, text="Nutrition Log", font=("Helvetica", 11), bg="#2196F3", fg="white", width=15, command=lambda: nutrition_screen(root, username)).grid(row=5, column=0, pady=5)
    # tk.Button(frame, text="Exercise Log", font=("Helvetica", 11), bg="#FF9800", fg="white", width=15, command=lambda: exercise_screen(root, username)).grid(row=5, column=1, pady=5)

    # tk.Button(frame, text="Weekly Chart", font=("Helvetica", 11), bg="#9C27B0", fg="white", width=32, command=lambda: show_weekly_plot(username)).grid(row=6, column=0, columnspan=2, pady=15)
