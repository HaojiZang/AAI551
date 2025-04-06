# Author: Haoji Zang, Linpeng Mao, Ruikang Li
# Date: 04/03/2025
# Description:

import os
from datetime import datetime

def today_str():
# 返回今天的日期字符串，格式如 "2025-04-03"
    pass

def get_user_data_path(username):
    return f"data/{username}_data.csv"

def get_nutrition_data_path(username):
    return f"data/{username}_nutrition.csv"

def get_exercise_data_path(username):
    return f"data/{username}_exercise.csv"

def ensure_data_file(username):
    # 初始化 data 文件夹和 csv
    pass

def read_csv_as_dict(filename):
    # 读取 csv 返回 dict 列表
    return []
