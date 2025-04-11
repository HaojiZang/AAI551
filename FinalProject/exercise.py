# Author: Ruikang Li
# Date: 04/06/2025
# Description: handles exercise data for the fitness tracker app

import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime

from utils.helpers import today_str, get_exercise_data_path, ensure_data_file, read_csv_as_dict


def exercise_screen(root, username):
    # 界面：输入活动、时长
    """
    Create the exercise tracking screen where users can log their exercises.
    
    :param root: The Tkinter root window
    :type root: tk.Tk
    :param username: The username of the current user
    :type username: str
    :return: None
    """
    # This is just a stub - the actual implementation will be in exercise_ui.py
    from exercise_ui import exercise_screen as show_exercise_ui
    show_exercise_ui(root, username)

def add_exercise_entry(username, activity, duration, calories):
    """
    Add a new exercise entry to the user's exercise log.
    
    :param username: The username of the current user
    :type username: str
    :param activity: The type of exercise performed
    :type activity: str
    :param duration: The duration of the exercise in minutes
    :type duration: float
    :param calories: The calories burned during the exercise
    :type calories: float
    :return: True if the entry was added successfully, False otherwise
    :rtype: bool
    """
    ensure_data_file(username)
    exercise_file = get_exercise_data_path(username)
    
    # Format data for storage
    date = today_str()
    
    # Check if all required fields are present
    if not all([activity, duration, calories]):
        return False
    
    try:
        # Convert duration and calories to appropriate types
        duration = float(duration)
        calories = float(calories)
        
        # Create a new entry
        new_entry = pd.DataFrame({
            'date': [date],
            'activity': [activity],
            'duration': [duration],
            'calories': [calories]
        })
        
        # If the file exists, append to it
        if os.path.isfile(exercise_file):
            df = pd.read_csv(exercise_file)
            df = pd.concat([df, new_entry], ignore_index=True)
        else:
            df = new_entry
        
        # Save the dataframe to CSV
        df.to_csv(exercise_file, index=False)
        
        return True
    
    except Exception as e:
        print(f"Error adding exercise entry: {e}")
        return False

def summarize_daily_exercise(username):
    """
    Calculate the total calories burned from exercises for the current day.
    
    :param username: The username of the current user
    :type username: str
    :return: Total calories burned today
    :rtype: float
    """
    exercise_file = get_exercise_data_path(username)
    
    # Return 0 if the file doesn't exist yet
    if not os.path.isfile(exercise_file):
        return 0.0
    
    try:
        # Read the exercise data
        df = pd.read_csv(exercise_file)
        
        # Filter for today's entries only
        today = today_str()
        today_df = df[df['date'] == today]
        
        # Sum the calories
        total_calories = today_df['calories'].sum()
        
        return float(total_calories)
    
    except Exception as e:
        print(f"Error summarizing daily exercise: {e}")
        return 0.0

def lookup_exercise_calories(activity, duration):
    r"""
    Look up the calories burned for a specific activity and duration based on reference data.
    
    :param activity: The type of exercise
    :type activity: str
    :param duration: The duration in minutes
    :type duration: float
    :return: Estimated calories burned
    :rtype: float
    """
    try:
        # Load the exercise dataset from the reference file
        reference_file = "reference/exercise_dataset.csv"
        
        # If the file doesn't exist, return a reasonable estimate
        if not os.path.isfile(reference_file):
            # Default fallback value - approx. 5 calories per minute for moderate activity
            return float(duration) * 5
        
        # Read the reference data
        df = pd.read_csv(reference_file)
        
        # The dataset is for 1 hour of activity, so we need to adjust for the duration
        # 1 hour = 60 minutes
        duration_hours = float(duration) / 60.0
        
        # Find the row for the specified activity - use case-insensitive partial matching
        activity_col = df.columns[0]  # The first column contains activity names
        
        # Try to find an exact match first (case-insensitive)
        matching_rows = df[df[activity_col].str.lower() == activity.lower()]
        
        # If no exact match, try for a partial match
        if matching_rows.empty:
            matching_rows = df[df[activity_col].str.lower().str.contains(activity.lower())]
        
        # If still no match, use a default value
        if matching_rows.empty:
            # Default fallback value - approx. 5 calories per minute for moderate activity
            return float(duration) * 5
        
        # Use the first matching row
        selected_activity = matching_rows.iloc[0]
        
        # Calculate calories based on a 155 lb reference person
        # This is a simplification - in a real app, you might want to use the user's weight
        calories_per_hour = selected_activity["155 lb"]
        
        # Adjust for the actual duration
        calories_burned = calories_per_hour * duration_hours
        
        return float(calories_burned)
    
    except Exception as e:
        print(f"Error looking up exercise calories: {e}")
        # Default fallback value
        return float(duration) * 5