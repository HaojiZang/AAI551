# Author: Linpeng Mao
# Date: 04/03/2025
# Description:
# 主控模块 tracker.py：
# 显示用户主界面，汇总今天的热量摄入、消耗、目标，并跳转到营养记录和运动记录界面。
# 提供对每日记录的保存、数据加载、当日汇总等功能接口

def tracker_screen(root, username):
# 构建主界面(Tkinter)
# 展示今天的热量摄入、消耗、目标
# 包含按钮跳转至：
# nutrition_screen(root, username)
# exercise_screen(root, username)
# show_weekly_plot(username)（趋势图）
    pass

def save_entry(username, in_cal, out_cal, goal):
# 写入一条数据到 <username>_data.csv
    pass

def load_recent_data(username, days):
# 返回最近几天的数据列表（字典格式）
# 用于绘制摄入/消耗/目标趋势图
    pass

def summarize_today(username):
# 从 <username>_data.csv 中提取今日数据
# 返回字典，如：
# {"calories_in": 2200, "calories_out": 400, "goal": 2000}
    pass

def open_nutrition_log(username):
# 用于打开 nutrition_screen() 打开饮食记录页面
    pass

def open_exercise_log(username):
# 用于打开 exercise_screen() 页面
    pass