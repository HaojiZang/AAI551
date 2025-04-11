# Author: Ruikang Li
# Date: 04/03/2025
# Description: This module provides the user interface for exercise tracking in the fitness tracker application.

import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from exercise import add_exercise_entry, lookup_exercise_calories
from utils.helpers import today_str, get_exercise_data_path

def exercise_screen(root, username):
    """
    Create the exercise tracking screen where users can log their exercises,
    durations, and see calorie expenditure.
    
    :param root: The Tkinter root window
    :type root: tk.Tk
    :param username: The username of the current user
    :type username: str
    :return: None
    """
    exercise_window = tk.Toplevel(root)
    exercise_window.title(f"Exercise Tracker - {username}")
    exercise_window.geometry("600x500")
    exercise_window.resizable(False, False)
    
    form_frame = ttk.LabelFrame(exercise_window, text="Log Exercise")
    form_frame.pack(padx=10, pady=10, fill="x")
    
    ttk.Label(form_frame, text="Activity:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    activity_var = tk.StringVar()
    activity_dropdown = ttk.Combobox(form_frame, textvariable=activity_var, width=30)
    
    activities = load_exercise_options()
    activity_dropdown['values'] = activities
    activity_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
    ttk.Label(form_frame, text="Duration (minutes):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    duration_var = tk.StringVar()
    ttk.Entry(form_frame, textvariable=duration_var, width=10).grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    def calculate_calories():
        """
        Calculate calories based on activity and duration inputs.
        
        :return: None
        """
        activity = activity_var.get()
        duration = duration_var.get()
        
        if not activity or not duration:
            messagebox.showerror("Error", "Please enter both activity and duration")
            return
        
        try:
            duration = float(duration)
            if duration <= 0:
                messagebox.showerror("Error", "Duration must be positive")
                return
            
            # Look up calories from reference data
            calories = lookup_exercise_calories(activity, duration)
            calories_var.set(f"{calories:.1f}")
            
        except ValueError:
            messagebox.showerror("Error", "Duration must be a number")
    
    calculate_btn = ttk.Button(form_frame, text="Calculate Calories", command=calculate_calories)
    calculate_btn.grid(row=1, column=2, padx=5, pady=5)
    
    ttk.Label(form_frame, text="Calories Burned:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    calories_var = tk.StringVar()
    ttk.Entry(form_frame, textvariable=calories_var, width=10, state="readonly").grid(row=2, column=1, padx=5, pady=5, sticky="w")
    
    def save_exercise():
        """
        Save the exercise entry to the user's data file.
        
        :return: None
        """
        activity = activity_var.get()
        duration = duration_var.get()
        calories = calories_var.get()
        
        if not activity or not duration or not calories:
            messagebox.showerror("Error", "Please complete all fields")
            return
        
        # Save the exercise entry
        success = add_exercise_entry(username, activity, duration, calories)
        
        if success:
            messagebox.showinfo("Success", "Exercise logged successfully")
            # Clear the form
            activity_var.set("")
            duration_var.set("")
            calories_var.set("")
            # Refresh the exercise history
            show_exercise_history(history_frame, username)
        else:
            messagebox.showerror("Error", "Failed to log exercise")
    
    save_btn = ttk.Button(form_frame, text="Save Exercise", command=save_exercise)
    save_btn.grid(row=3, column=1, padx=5, pady=10)
    
    history_frame = ttk.LabelFrame(exercise_window, text="Today's Exercise History")
    history_frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    show_exercise_history(history_frame, username)
    
    def show_visualization():
        """
        Show the exercise visualization.
        
        :return: None
        """
        try:
            # Import here to avoid circular imports
            from visualize import show_exercise_plot
            show_exercise_plot(username)
        except Exception as e:
            messagebox.showerror("Error", f"Could not display visualization: {e}")
    
    viz_btn = ttk.Button(exercise_window, text="Show Exercise Trends", command=show_visualization)
    viz_btn.pack(padx=10, pady=10)
    
    # Close button
    close_btn = ttk.Button(exercise_window, text="Close", command=exercise_window.destroy)
    close_btn.pack(padx=10, pady=10)

def show_exercise_history(frame, username):
    """
    Display today's exercise history in the provided frame.
    
    :param frame: The Tkinter frame to display the history in
    :type frame: ttk.Frame
    :param username: The current username
    :type username: str
    :return: None
    """
    for widget in frame.winfo_children():
        widget.destroy()
    
    columns = ("Time", "Activity", "Duration", "Calories")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True, padx=5, pady=5)
    
    exercise_file = get_exercise_data_path(username)
    today = today_str()
    
    if os.path.isfile(exercise_file):
        try:
            df = pd.read_csv(exercise_file)
            today_entries = df[df['date'] == today]
            
            if today_entries.empty:
                tree.insert("", "end", values=("No exercise logged today", "", "", ""))
            else:
                for _, row in today_entries.iterrows():
                    activity = row['activity']
                    duration = row['duration']
                    calories = row['calories']
                    
                    duration_str = f"{float(duration):.1f} min"
                    calories_str = f"{float(calories):.1f} cal"
                    
                    tree.insert("", "end", values=(today, activity, duration_str, calories_str))
        
        except Exception as e:
            print(f"Error loading exercise history: {e}")
            tree.insert("", "end", values=(f"Error: {e}", "", "", ""))
    else:
        # File doesn't exist yet
        tree.insert("", "end", values=("No exercise logged today", "", "", ""))

def load_exercise_options():
    """
    Load exercise options from the reference file using pandas.
    
    :return: List of exercise activities
    :rtype: list
    """
    reference_file = "reference/exercise_dataset.csv"
    
    default_options = ["Walking", "Running", "Cycling", "Swimming", "Weightlifting", "Yoga", "HIIT", "Other"]
    
    if not os.path.isfile(reference_file):
        return default_options
    
    try:
        df = pd.read_csv(reference_file)
        activities = df.iloc[:, 0].tolist()  # First column contains activity names
        return activities if activities else default_options
    
    except Exception as e:
        print(f"Error loading exercise options: {e}")
        return default_options