# Author: Haoji Zang
# Date: 04/03/2025
# Description: This module defines the NutritionTracker class for managing user nutrition data.

import csv
import pandas as pd
from utils.helpers import get_nutrition_data_path
from utils.helpers import today_str

class NutritionTracker:
    def __init__(self):
        # Load the data of food (Calories)
        food_file_path = "reference/Food and Calories.csv"
        # Use pandas read .csv file
        food_data = pd.read_csv(food_file_path)
        # Creat a dic to save {food, Calories}
        self.food_map = {}

        # Fill the dictionary with data from the Food and Calories.csv
        for index, row in food_data.iterrows():
            name = row["Food"]
            calories = row["Calories_per_100g"]
            self.food_map[name.strip().title()] = calories

    def calculate_calories(self, food_name, grams):
        """
        Calculate total calories based on food name and weight (grams).

        Parameters:
            food_name (str): The name of the food (e.g., 'banana')
            grams (float): The weight of the food in grams
        """
        name = food_name.strip().title()
        if name in self.food_map:
            calories_per_100g = self.food_map[name]
        else:
            print(f"Warning: '{name}' not found in reference table.")
            calories_per_100g = 0

        # Calculate real Calories
        total_calories = calories_per_100g * grams / 100
        return round(total_calories, 2)

    def add_food_entry(self, username, food_name, grams):
        """
        Add a food consumption record to the user's nutrition CSV file.

        Parameters:
            username (str): The name of the user.
            food_name (str): The name of the food consumed.
            grams (float): The amount of food in grams.
        """
        # Calculate total calories
        calories = self.calculate_calories(food_name, grams)
        # Get the user's nutrition data path
        file_path = get_nutrition_data_path(username)

        # Build one row of data
        new_row = {
            "date": today_str(),
            "food": food_name.strip(),
            "grams": grams,
            "calories": calories
        }

        # Append to CSV
        df = pd.DataFrame([new_row])
        df.to_csv(file_path, mode="a", header=False, index=False)

    def summarize_daily_nutrition(self, username):
        """
        Calculate total calories consumed today for the user.

        Parameters:
            username (str): The user's name.
        """
        # Get the path to the user's nutrition CSV file
        file_path = get_nutrition_data_path(username)
        # Get today's date as a string (format: YYYY-MM-DD)
        today = today_str()
        # Initialize total calorie counter
        total = 0

        try:
            # Read all rows
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                # Check if row exists and is from today
                for row in reader:
                    if row and row[0] == today:
                        # Accumulate calories
                        total += float(row[3])
        except FileNotFoundError:
            pass

        # Return total calories
        return {"calories": round(total, 2)}

    def clear_today_nutrition(self, username):
        """
        Remove all nutrition records from today's date for the given user.

        Parameters:
            username (str): The user's name.
        """
        file_path = get_nutrition_data_path(username)
        today = today_str()
        remaining_rows = []

        try:
            # Read all rows
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                #  Keep only rows that are not from today
                for row in reader:
                    if row and row[0] != today:
                        remaining_rows.append(row)

            # Write the remaining rows back to the file
            with open(file_path, "w") as file:
                writer = csv.writer(file)
                writer.writerows(remaining_rows)

        except FileNotFoundError:
            # If the file doesn't exist, do nothing
            pass

    def get_today_entries(self, username):
        """
        Retrieve all nutrition entries from today's date for the given user.

        Parameters:
            username (str): The user's name.
        """
        file_path = get_nutrition_data_path(username)
        today = today_str()
        today_entries = []

        try:
            # Read all rows
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                # Collect today's date
                for row in reader:
                    if row and row[0] == today:
                        today_entries.append(row)
        except FileNotFoundError:
            pass

        return today_entries
