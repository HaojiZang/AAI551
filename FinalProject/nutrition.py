# Author: Haoji Zang
# Date: 04/03/2025
# Description: This module defines the NutritionTracker class for managing user nutrition data.


import csv
import os
import pandas as pd
from utils.helpers import get_nutrition_data_path
from utils.helpers import today_str


class NutritionTracker:
    def __init__(self):
        food_file_path = "reference/Food and Calories.csv"
        food_data = pd.read_csv(food_file_path)
        self.food_map = {}

        for index, row in food_data.iterrows():
            name = row["Food"]
            calories = row["Calories_per_100g"]
            self.food_map[name.strip().title()] = calories

    def calculate_calories(self, food_name, grams):
        name = food_name.strip().title()
        calories_per_100g = self.food_map.get(name, 0)
        return round(calories_per_100g * grams / 100, 2)

    def add_food_entry(self, username, food_name, grams, date=None):
        if date is None:
            date = today_str()
        calories = self.calculate_calories(food_name, grams)
        file_path = get_nutrition_data_path(username)

        new_row = {
            "username": username,
            "date": date,
            "food": food_name.strip(),
            "grams": grams,
            "calories": calories
        }

        df = pd.DataFrame([new_row])
        df.to_csv(file_path, mode="a", header=not os.path.exists(file_path), index=False)

    def summarize_daily_nutrition(self, username, target_date=None):
        file_path = get_nutrition_data_path(username)
        if target_date is None:
            target_date = today_str()
        total = 0

        try:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["date"] == target_date and row["username"] == username:
                        total += float(row["calories"])
        except FileNotFoundError:
            pass

        return {"calories": round(total, 2)}

    def clear_today_nutrition(self, username):
        file_path = get_nutrition_data_path(username)
        today = today_str()
        new_rows = []

        try:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if not (row["username"] == username and row["date"] == today):
                        new_rows.append(row)
            if new_rows:
                keys = new_rows[0].keys()
                with open(file_path, "w", newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(new_rows)
            else:
                os.remove(file_path)
        except FileNotFoundError:
            pass

    def get_today_entries(self, username):
        file_path = get_nutrition_data_path(username)
        today = today_str()
        entries = []

        try:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["username"] == username and row["date"] == today:
                        entries.append(row)
        except FileNotFoundError:
            pass

        return entries

