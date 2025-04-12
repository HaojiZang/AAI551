# Author: Ruikang Li
# Date: 04/11/2025
# Description: This module provides the user interface for exercise tracking in the fitness tracker application.

import os
import csv
import time
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from exercise import add_exercise_entry, lookup_exercise_calories
from utils.helpers import today_str, get_exercise_data_path

_cached_activities = None

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
    exercise_window.geometry("600x600")
    exercise_window.resizable(True, True)
    
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
    duration_entry = ttk.Entry(form_frame, textvariable=duration_var, width=10)
    duration_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    ttk.Label(form_frame, text="Calories Burned:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    calories_var = tk.StringVar()
    calories_entry = ttk.Entry(form_frame, textvariable=calories_var, width=10, state="readonly")
    calories_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    
    def calculate_calories():
        """
        Calculate calories based on activity and duration inputs.
        
        :return: None
        """
        start_time = time.time()
        
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
            
            calories = lookup_exercise_calories(activity, duration)
            calories_var.set(f"{calories:.1f}")
            
            save_btn.focus_set()
            
        except ValueError:
            messagebox.showerror("Error", "Duration must be a number")
        
        end_time = time.time()
        print(f"calculate_calories took {end_time - start_time:.4f} seconds")
    
    calculate_btn = ttk.Button(form_frame, text="Calculate Calories", command=calculate_calories)
    calculate_btn.grid(row=1, column=2, padx=5, pady=5)
    
    def save_exercise():
        """
        Save the exercise entry to the user's data file.
        
        :return: None
        """
        start_time = time.time()
        
        activity = activity_var.get()
        duration = duration_var.get()
        calories = calories_var.get()
        
        if not activity or not duration or not calories:
            messagebox.showerror("Error", "Please complete all fields")
            return
        
        success = add_exercise_entry(username, activity, duration, calories)
        
        if success:
            messagebox.showinfo("Success", "Exercise logged successfully")
            activity_var.set("")
            duration_var.set("")
            calories_var.set("")
            show_exercise_history(history_frame, username)
            activity_dropdown.focus_set()
        else:
            messagebox.showerror("Error", "Failed to log exercise")
        
        end_time = time.time()
        print(f"save_exercise took {end_time - start_time:.4f} seconds to execute")
    
    save_btn = ttk.Button(form_frame, text="Save Exercise", command=save_exercise)
    save_btn.grid(row=3, column=1, padx=5, pady=10)
    
    history_frame = ttk.LabelFrame(exercise_window, text="Today's Exercise History")
    history_frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    show_exercise_history(history_frame, username)
    
    status_var = tk.StringVar()
    status_label = ttk.Label(exercise_window, textvariable=status_var, anchor="w")
    status_label.pack(side="bottom", fill="x", padx=10, pady=5)
    
    button_frame = ttk.Frame(exercise_window)
    button_frame.pack(side="bottom", fill="x", padx=10, pady=10)
    
    def show_visualization():
        """
        Show the exercise visualization with improved feedback.
        
        :return: None
        """
        start_time = time.time()
        
        status_var.set("Loading visualization...")
        exercise_window.update_idletasks()
        
        try:
            from visualize import show_exercise_plot
            show_exercise_plot(username)
            status_var.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Could not display visualization: {e}")
            status_var.set("")
        
        end_time = time.time()
        print(f"show_visualization took {end_time - start_time:.4f} seconds")
    
    try:
        viz_btn = ttk.Button(button_frame, text="Show Exercise Trends", command=show_visualization)
        viz_btn.pack(side="left", padx=10, pady=10)
        print("Visualization button created successfully")
    except Exception as e:
        print(f"Error creating visualization button: {e}")
    
    close_btn = ttk.Button(button_frame, text="Close", command=exercise_window.destroy)
    close_btn.pack(side="right", padx=10, pady=10)
    
    activity_dropdown.focus_set()
    
    activity_dropdown.bind("<Return>", lambda e: duration_entry.focus_set())
    duration_entry.bind("<Return>", lambda e: calculate_btn.invoke())
    calculate_btn.bind("<Return>", lambda e: save_btn.focus_set())
    save_btn.bind("<Return>", lambda e: save_btn.invoke())
    
    def select_all(event):
        event.widget.select_range(0, 'end')
        return "break"
    
    duration_entry.bind("<FocusIn>", select_all)
    
    print("Widgets in exercise window:")
    for widget in exercise_window.winfo_children():
        print(f"Widget: {widget}, Visible: {widget.winfo_viewable()}")

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
        tree.insert("", "end", values=("No exercise logged today", "", "", ""))

def load_exercise_options():
    """
    Load exercise options from the reference file using pandas.
    
    :return: List of exercise activities
    :rtype: list
    """
    global _cached_activities
    
    if _cached_activities is not None:
        return _cached_activities
    
    reference_file = "reference/exercise_dataset.csv"
    
    default_options = ["Walking", "Running", "Cycling", "Swimming", "Weightlifting", "Yoga", "HIIT", "Other"]
    
    if not os.path.isfile(reference_file):
        _cached_activities = default_options
        return default_options
    
    try:
        df = pd.read_csv(reference_file)
        activities = df.iloc[:, 0].tolist()
        _cached_activities = activities if activities else default_options
        return _cached_activities
    
    except Exception as e:
        print(f"Error loading exercise options: {e}")
        _cached_activities = default_options
        return default_options