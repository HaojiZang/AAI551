# Author: Ruikang Li
# Date: 04/11/2025
# Description: user interface for exercise tracking in the fitness tracker application

import time
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

from exercise import ExerciseTracker
from utils.helpers import today_str


class ExerciseUI:
    """
    Class that provides the user interface for exercise tracking in the fitness tracker application.
    """
    
    def __init__(self, root, username):
        """
        Initialize the ExerciseUI class and create the exercise tracking window.
        
        :param root: The Tkinter root window
        :type root: tk.Tk
        :param username: The username of the current user
        :type username: str
        """
        self.root = root
        self.username = username
        self.exercise_tracker = ExerciseTracker()
        
        self.exercise_window = None
        self.activity_var = None
        self.duration_var = None
        self.calories_var = None
        self.status_var = None
        
        # Create and populate the exercise window
        self.create_exercise_window()
    
    def create_exercise_window(self):
        """
        Create the exercise tracking window with all UI elements.
        
        :return: None
        """
        self.exercise_window = tk.Toplevel(self.root)
        self.exercise_window.title(f"Exercise Tracker - {self.username}")
        self.exercise_window.geometry("600x600")
        self.exercise_window.resizable(True, True)
        
        self.create_form_frame()
        
        self.history_frame = ttk.LabelFrame(self.exercise_window, text="Today's Exercise History")
        self.history_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.show_exercise_history()
        
        self.status_var = tk.StringVar()
        status_label = ttk.Label(self.exercise_window, textvariable=self.status_var, anchor="w")
        status_label.pack(side="bottom", fill="x", padx=10, pady=5)
        
        self.create_button_frame()
    
    def create_form_frame(self):
        """
        Create the form frame with input elements for logging exercises.
        
        :return: None
        """
        form_frame = ttk.LabelFrame(self.exercise_window, text="Log Exercise")
        form_frame.pack(padx=10, pady=10, fill="x")
        
        ttk.Label(form_frame, text="Activity:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.activity_var = tk.StringVar()
        activity_dropdown = ttk.Combobox(form_frame, textvariable=self.activity_var, width=30)
        
        activities = self.exercise_tracker.get_exercise_options()
        activity_dropdown['values'] = activities
        activity_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(form_frame, text="Duration (minutes):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.duration_var = tk.StringVar()
        duration_entry = ttk.Entry(form_frame, textvariable=self.duration_var, width=10)
        duration_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(form_frame, text="Calories Burned:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.calories_var = tk.StringVar()
        calories_entry = ttk.Entry(form_frame, textvariable=self.calories_var, width=10, state="readonly")
        calories_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        calculate_btn = ttk.Button(form_frame, text="Calculate Calories", command=self.calculate_calories)
        calculate_btn.grid(row=1, column=2, padx=5, pady=5)
        
        save_btn = ttk.Button(form_frame, text="Save Exercise", command=self.save_exercise)
        save_btn.grid(row=3, column=1, padx=5, pady=10)
        
        # Set up keyboard navigation
        activity_dropdown.focus_set()
        activity_dropdown.bind("<Return>", lambda e: duration_entry.focus_set())
        duration_entry.bind("<Return>", lambda e: calculate_btn.invoke())
        calculate_btn.bind("<Return>", lambda e: save_btn.focus_set())
        save_btn.bind("<Return>", lambda e: save_btn.invoke())
        
        def select_all(event):
            event.widget.select_range(0, 'end')
            return "break"
        
        duration_entry.bind("<FocusIn>", select_all)
        
        self.form_frame = form_frame
        self.activity_dropdown = activity_dropdown
        self.duration_entry = duration_entry
        self.save_btn = save_btn
    
    def create_button_frame(self):
        """
        Create the button frame with action buttons.
        
        :return: None
        """
        button_frame = ttk.Frame(self.exercise_window)
        button_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        try:
            viz_btn = ttk.Button(button_frame, text="Show Exercise Trends", command=self.show_visualization)
            viz_btn.pack(side="left", padx=10, pady=10)
            print("Visualization button created successfully")
        except Exception as e:
            print(f"Error creating visualization button: {e}")
        
        close_btn = ttk.Button(button_frame, text="Close", command=self.exercise_window.destroy)
        close_btn.pack(side="right", padx=10, pady=10)
    
    def calculate_calories(self):
        """
        Calculate calories based on activity and duration inputs.
        
        :return: None
        """
        start_time = time.time()
        
        activity = self.activity_var.get()
        duration = self.duration_var.get()
        
        if not activity or not duration:
            messagebox.showerror("Error", "Please enter both activity and duration")
            return
        
        try:
            duration = float(duration)
            if duration <= 0:
                messagebox.showerror("Error", "Duration must be positive")
                return
            
            calories = self.exercise_tracker.lookup_exercise_calories(activity, duration)
            self.calories_var.set(f"{calories:.1f}")
            
            self.save_btn.focus_set()
            
        except ValueError:
            messagebox.showerror("Error", "Duration must be a number")
        
        end_time = time.time()
        print(f"calculate_calories took {end_time - start_time:.4f} seconds")
    
    def save_exercise(self):
        """
        Save the exercise entry to the user's data file.
        
        :return: None
        """
        start_time = time.time()
        
        activity = self.activity_var.get()
        duration = self.duration_var.get()
        calories = self.calories_var.get()
        
        if not activity or not duration or not calories:
            messagebox.showerror("Error", "Please complete all fields")
            return
        
        success = self.exercise_tracker.add_exercise_entry(self.username, activity, duration, calories)
        
        if success:
            messagebox.showinfo("Success", "Exercise logged successfully")
            self.activity_var.set("")
            self.duration_var.set("")
            self.calories_var.set("")
            self.show_exercise_history()
            self.activity_dropdown.focus_set()
        else:
            messagebox.showerror("Error", "Failed to log exercise")
        
        end_time = time.time()
        print(f"save_exercise took {end_time - start_time:.4f} seconds to execute")
    
    def show_exercise_history(self):
        """
        Display today's exercise history in the history frame.
        
        :return: None
        """
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        columns = ("Time", "Activity", "Duration", "Calories")
        tree = ttk.Treeview(self.history_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        today_entries = self.exercise_tracker.get_today_exercise_entries(self.username)
        today = today_str()
        
        if today_entries is None or today_entries.empty:
            tree.insert("", "end", values=("No exercise logged today", "", "", ""))
        else:
            for _, row in today_entries.iterrows():
                activity = row['activity']
                duration = row['duration']
                calories = row['calories']
                
                duration_str = f"{float(duration):.1f} min"
                calories_str = f"{float(calories):.1f} cal"
                
                tree.insert("", "end", values=(today, activity, duration_str, calories_str))
    
    def show_visualization(self):
        """
        Show the exercise visualization with improved feedback.
        
        :return: None
        """
        start_time = time.time()
        
        self.status_var.set("Loading visualization...")
        self.exercise_window.update_idletasks()
        
        try:
            from visualize import show_exercise_plot
            show_exercise_plot(self.username)
            self.status_var.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Could not display visualization: {e}")
            self.status_var.set("")
        
        end_time = time.time()
        print(f"show_visualization took {end_time - start_time:.4f} seconds")


def exercise_screen(root, username):
    """
    Wrapper function for backward compatibility.
    Creates an ExerciseUI instance.
    
    :param root: The Tkinter root window
    :type root: tk.Tk
    :param username: The username of the current user
    :type username: str
    :return: None
    """
    ExerciseUI(root, username)