# Author: Haoji Zang, Linpeng Mao, Ruikang Li
# Date: 04/03/2025
# Description:

import csv
import os
from datetime import datetime

def today_str():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d')

def get_user_data_path(username):
    return os.path.join("data", f"{username}_data.csv")

def get_nutrition_data_path(username):
    return f"data/{username}_nutrition.csv"

def get_exercise_data_path(username):
    return f"data/{username}_exercise.csv"

def ensure_data_file(username):
    """Ensure that the user's main data file exists and has a header"""
    path = get_user_data_path(username)
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(path):
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["date", "in_cal", "out_cal", "goal"])

def read_csv_as_dict(filename):
    # 读取 csv 返回 dict 列表
    return []
