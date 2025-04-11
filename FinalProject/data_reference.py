# Author: Ruikang Li
# Date: 04/08/2025
# Description: This module handles loading reference data for exercises and nutrition.

import os
import pandas as pd

def load_exercise_reference():
    """
    Load the exercise reference data from CSV file.
    
    :return: A dictionary mapping exercise names to calorie information
    :rtype: dict
    """
    reference_file = "reference/exercise_dataset.csv"
    
    if not os.path.isfile(reference_file):
        return {}
    
    try:
        df = pd.read_csv(reference_file)
        
        result = {}
        for _, row in df.iterrows():
            activity = row.iloc[0]  # First column contains activity names
            result[activity] = {
                '130_lb': row.iloc[1],
                '155_lb': row.iloc[2],
                '180_lb': row.iloc[3],
                '205_lb': row.iloc[4],
                'calories_per_kg': row.iloc[5]
            }
        
        return result
    
    except Exception as e:
        print(f"Error loading exercise reference data: {e}")
        return {}

def load_food_reference():
    """
    Load the food reference data from CSV file.
    
    :return: A dictionary mapping food names to nutrition information
    :rtype: dict
    """
    # TODO (Haoji Zang)
    return {}