# Author: Haoji Zang
# Date: 04/03/2025
# Description: Nutrition UI with total calorie display.

import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from nutrition import NutritionTracker

class NutritionUI:
    def __init__(self, root, username):
        self.username = username
        self.tracker = NutritionTracker()
        self.goal = 2000

        self.root = tk.Toplevel(root)
        self.root.title("Nutrition Tracker")
        self.root.geometry("430x600")

        food_df = pd.read_csv("reference/Food and Calories.csv")
        self.food_list = food_df["Food"].tolist()

        self.build_ui()
        self.refresh_summary()

    def build_ui(self):
        tk.Label(self.root, text="Enter food name:").pack()
        self.food_entry = tk.Entry(self.root)
        self.food_entry.pack(pady=3)

        tk.Label(self.root, text="Enter weight in grams:").pack()
        self.grams_entry = tk.Entry(self.root)
        self.grams_entry.pack(pady=3)

        tk.Label(self.root, text="Enter date (YYYY-MM-DD):").pack()
        self.date_entry = tk.Entry(self.root)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.date_entry.pack(pady=3)

        tk.Button(self.root, text="Save Entry", command=self.save_entry).pack(pady=10)
        tk.Button(self.root, text="Show Available Food List", command=self.show_food_list).pack(pady=5)

        self.total_label = tk.Label(self.root, text="")
        self.total_label.pack(pady=5)

        tk.Button(self.root, text="Clear Today's Records", command=self.clear_today_data).pack(pady=5)
        tk.Button(self.root, text="Export Today's Records", command=self.export_today).pack(pady=5)
        tk.Button(self.root, text="Show Weekly Intake Trend", command=self.show_trend).pack(pady=5)
        tk.Button(self.root, text="Show Monthly Summary", command=self.show_month_summary).pack(pady=5)
        tk.Button(self.root, text="Show Yearly Summary", command=self.show_year_summary).pack(pady=5)

    def save_entry(self):
        try:
            food = self.food_entry.get()
            grams = float(self.grams_entry.get())
            date = self.date_entry.get().strip()
            datetime.strptime(date, '%Y-%m-%d')  # 校验格式

            if grams <= 0 or not food.strip():
                raise ValueError

            self.tracker.add_food_entry(self.username, food.strip(), grams, date)
            messagebox.showinfo("Success", f"Saved: {food.strip()} - {grams}g on {date}")

            self.food_entry.delete(0, tk.END)
            self.grams_entry.delete(0, tk.END)
            self.refresh_summary()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid food, date (YYYY-MM-DD), and positive weight.")

    def refresh_summary(self):
        today = datetime.today().strftime('%Y-%m-%d')
        total = self.tracker.summarize_daily_nutrition(self.username, today)
        kcal = total['calories']
        self.total_label.config(text=f"Total calories today: {kcal} / Goal: {self.goal}")
        self.total_label.config(fg="red" if kcal > self.goal else "green")

    def clear_today_data(self):
        self.tracker.clear_today_nutrition(self.username)
        messagebox.showinfo("Cleared", "Today's nutrition records have been cleared.")
        self.refresh_summary()

    def export_today(self):
        entries = self.tracker.get_today_entries(self.username)
        if not entries:
            messagebox.showinfo("Notice", "No records found for today.")
            return
        text = "Today's Nutrition:\n"
        for row in entries:
            text += f"{row['food']} - {row['grams']}g - {row['calories']} kcal\n"
        messagebox.showinfo("Today's Records", text)

    def show_food_list(self):
        win = tk.Toplevel(self.root)
        win.title("Available Food List")
        win.geometry("300x400")
        scrollbar = tk.Scrollbar(win)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox = tk.Listbox(win, yscrollcommand=scrollbar.set)
        for food in sorted(self.food_list):
            listbox.insert(tk.END, food)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

    def show_trend(self):
        today = datetime.today()
        dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
        values = [self.tracker.summarize_daily_nutrition(self.username, d)['calories'] for d in dates]

        plt.figure(figsize=(8, 4))
        plt.plot(dates, values, marker='o')
        plt.title("7-Day Calorie Intake Trend")
        plt.xlabel("Date")
        plt.ylabel("Calories")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def show_month_summary(self):
        year = simpledialog.askstring("Input", "Enter year (e.g., 2025):", parent=self.root)
        month = simpledialog.askstring("Input", "Enter month (1-12):", parent=self.root)

        try:
            year = int(year)
            month = int(month)
            days_in_month = (datetime(year, month % 12 + 1, 1) - timedelta(days=1)).day
        except:
            messagebox.showerror("Error", "Invalid year or month.")
            return

        dates = [f"{year}-{month:02d}-{day:02d}" for day in range(1, days_in_month + 1)]
        values = [self.tracker.summarize_daily_nutrition(self.username, d)['calories'] for d in dates]

        plt.figure(figsize=(10, 4))
        plt.plot(dates, values, marker='o')
        plt.title(f"{datetime(year, month, 1).strftime('%B %Y')} Calorie Intake")
        plt.xlabel("Day")
        plt.ylabel("Calories")
        plt.xticks(rotation=45, fontsize=8)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def show_year_summary(self):
        year = simpledialog.askstring("Input", "Enter year (e.g., 2025):", parent=self.root)
        try:
            year = int(year)
        except:
            messagebox.showerror("Error", "Invalid year.")
            return

        months = [f"{year}-{m:02d}" for m in range(1, 13)]
        monthly_totals = []

        for ym in months:
            total = 0
            for day in range(1, 32):
                try:
                    date_str = f"{ym}-{day:02d}"
                    total += self.tracker.summarize_daily_nutrition(self.username, date_str)['calories']
                except:
                    continue
            monthly_totals.append(total)

        plt.figure(figsize=(10, 5))
        plt.bar(range(1, 13), monthly_totals, tick_label=[datetime(year, m, 1).strftime('%b') for m in range(1, 13)])
        plt.title(f"{year} Monthly Calorie Summary")
        plt.xlabel("Month")
        plt.ylabel("Total Calories")
        plt.grid(axis="y")
        plt.tight_layout()
        plt.show()

# Wrapper function (if needed by external modules)
def nutrition_screen(root, username):
    NutritionUI(root, username)