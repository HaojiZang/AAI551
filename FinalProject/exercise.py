# Author: Ruikang Li
# Date: 04/06/2025
# Description: handles exercise data for the fitness tracker app

import os
import csv
import pandas as pd

from utils.helpers import today_str, get_exercise_data_path, ensure_data_file


class ExerciseTracker:
    """
    Class that handles all exercise tracking functionality including adding entries,
    looking up calorie burn, and summarizing daily exercise.
    """
    
    def __init__(self):
        """
        Initialize the ExerciseTracker class.
        """
        self.reference_file = "reference/exercise_dataset.csv"
        
    def add_exercise_entry(self, username, activity, duration, calories):
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
        
        date = today_str()
        
        if not all([activity, duration, calories]):
            return False
        
        try:
            duration = float(duration)
            calories = float(calories)
            
            new_entry = pd.DataFrame({
                'date': [date],
                'activity': [activity],
                'duration': [duration],
                'calories': [calories]
            })
            
            if os.path.isfile(exercise_file):
                df = pd.read_csv(exercise_file)
                for col in df.columns:
                    if col in new_entry:
                        # Convert to the same dtype to avoid the warning
                        new_entry[col] = new_entry[col].astype(df[col].dtype)
                
                df = pd.concat([df, new_entry], ignore_index=True)
            else:
                df = new_entry
            
            df.to_csv(exercise_file, index=False)
            
            return True
        
        except Exception as e:
            print(f"Error adding exercise entry: {e}")
            return False

    def summarize_daily_exercise(self, username):
        """
        Calculate the total calories burned from exercises for the current day.
        
        :param username: The username of the current user
        :type username: str
        :return: Total calories burned today
        :rtype: float
        """
        exercise_file = get_exercise_data_path(username)
        
        if not os.path.isfile(exercise_file):
            return 0.0
        
        try:
            df = pd.read_csv(exercise_file)
            
            today = today_str()
            today_df = df[df['date'] == today]
            
            total_calories = today_df['calories'].sum()
            
            return float(total_calories)
        
        except Exception as e:
            print(f"Error summarizing daily exercise: {e}")
            return 0.0

    def lookup_exercise_calories(self, activity, duration):
        """
        Look up the calories burned for a specific activity and duration based on reference data.
        
        :param activity: The type of exercise
        :type activity: str
        :param duration: The duration in minutes
        :type duration: float
        :return: Estimated calories burned
        :rtype: float
        """
        try:
            if not os.path.isfile(self.reference_file):
                # Default fallback value - approx. 5 calories per minute for moderate activity
                return float(duration) * 5
            
            df = pd.read_csv(self.reference_file)
            
            duration_hours = float(duration) / 60.0
            
            activity_col = df.columns[0]
            
            matching_rows = df[df[activity_col].str.lower() == activity.lower()]
            
            if matching_rows.empty:
                matching_rows = df[df[activity_col].str.lower().str.contains(activity.lower())]
            
            if matching_rows.empty:
                #approx. 5 calories per minute for moderate activity
                return float(duration) * 5
            
            selected_activity = matching_rows.iloc[0]
            
            calories_per_hour = selected_activity["155 lb"]
            
            calories_burned = calories_per_hour * duration_hours
            
            return float(calories_burned)
        
        except Exception as e:
            print(f"Error looking up exercise calories: {e}")
            return float(duration) * 5
            
    def get_exercise_options(self):
        """
        Load exercise options from the reference file using pandas.
        
        :return: List of exercise activities
        :rtype: list
        """
        default_options = ["Walking", "Running", "Cycling", "Swimming", "Weightlifting", "Yoga", "HIIT", "Other"]
        
        if not os.path.isfile(self.reference_file):
            return default_options
        
        try:
            df = pd.read_csv(self.reference_file)
            activities = df.iloc[:, 0].tolist()
            return activities if activities else default_options
        
        except Exception as e:
            print(f"Error loading exercise options: {e}")
            return default_options
            
    def get_today_exercise_entries(self, username):
        """
        Get today's exercise entries for the specified user.
        
        :param username: The username of the current user
        :type username: str
        :return: DataFrame of today's entries or None if no entries exist
        :rtype: pandas.DataFrame or None
        """
        exercise_file = get_exercise_data_path(username)
        today = today_str()
        
        if not os.path.isfile(exercise_file):
            return None
            
        try:
            df = pd.read_csv(exercise_file)
            today_entries = df[df['date'] == today]
            
            if today_entries.empty:
                return None
                
            return today_entries
            
        except Exception as e:
            print(f"Error getting today's exercise entries: {e}")
            return None


def exercise_screen(root, username):
    """
    Create the exercise tracking screen where users can log their exercises.
    Wrapper function for backward compatibility.
    
    :param root: The Tkinter root window
    :type root: tk.Tk
    :param username: The username of the current user
    :type username: str
    :return: None
    """
    from exercise_ui import ExerciseUI
    exercise_ui = ExerciseUI(root, username)