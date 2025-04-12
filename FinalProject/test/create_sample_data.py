# Author: Ruikang Li
# Date: 04/11/2025
# Description: Create the sample test data based on the real data structure.

import pandas as pd
import os
import sys
import pathlib

current_dir = pathlib.Path(__file__).parent.absolute()
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Create a sample exercise dataset based on the actual structure
data = {
    "Activity, Exercise or Sport (1 hour)": [
        "Running, 5 mph (12 min/mile)",
        "Running, 7.5 mph (8 min/mile)",
        "Walking, 3 mph (20 min/mile)",
        "Walking, 4 mph (15 min/mile)",
        "Cycling, moderate effort",
        "Cycling, vigorous effort",
        "Swimming, freestyle, moderate",
        "Swimming, freestyle, vigorous",
        "Yoga, Hatha",
        "Weight Lifting, vigorous",
        "Basketball, playing a game",
        "Soccer, casual",
        "Tennis, singles",
        "Hiking, cross country"
    ],
    "130 lb": [472, 680, 236, 295, 354, 590, 413, 590, 236, 354, 472, 413, 472, 354],
    "155 lb": [563, 810, 281, 352, 422, 704, 493, 704, 281, 422, 563, 493, 563, 422],
    "180 lb": [654, 941, 327, 409, 490, 817, 572, 817, 327, 490, 654, 572, 654, 490],
    "205 lb": [745, 1071, 372, 465, 558, 931, 651, 931, 372, 558, 745, 651, 745, 558],
    "Calories per kg": [8.5, 12.3, 4.3, 5.4, 6.8, 11.4, 7.8, 11.2, 4.3, 6.8, 8.5, 7.8, 8.5, 6.8]
}

df = pd.DataFrame(data)

csv_path = os.path.join(parent_dir, "reference", "exercise_dataset.csv")
df.to_csv(csv_path, index=False)
print(f"Created sample exercise dataset at {csv_path}")