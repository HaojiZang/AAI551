# Author: Haoji Zang, Ruikang Li
# Date: 05/02/2025
# Description: Tests for the nutrition tracking functionality

import os
import sys
import pytest
import pandas as pd
from datetime import datetime
import tempfile
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nutrition import NutritionTracker
from utils.helpers import today_str, get_nutrition_data_path

class TestNutritionTracker:
    """Test class for NutritionTracker functionality"""
    
    @pytest.fixture
    def setup_environment(self, monkeypatch):
        """Fixture to set up a test environment with mocked paths"""
        self.test_dir = tempfile.mkdtemp()
        
        # test food data
        test_food_data = {
            "Food": ["Apple", "Banana", "Chicken Breast", "Rice", "Broccoli"],
            "Calories_per_100g": [52, 89, 165, 130, 34]
        }
        
        # temporary food reference file
        self.test_food_file = os.path.join(self.test_dir, "Food and Calories.csv")
        pd.DataFrame(test_food_data).to_csv(self.test_food_file, index=False)
        
        def mock_get_nutrition_data_path(username):
            return os.path.join(self.test_dir, f"{username}_nutrition.csv")
        
        monkeypatch.setattr('utils.helpers.get_nutrition_data_path', mock_get_nutrition_data_path)
        
        original_init = NutritionTracker.__init__
        
        def mock_init(self_tracker):
            """Mocked __init__ method that uses test food file"""
            food_file_path = self.test_food_file
            food_data = pd.read_csv(food_file_path)
            self_tracker.food_map = {}
            
            for index, row in food_data.iterrows():
                name = row["Food"]
                calories = row["Calories_per_100g"]
                self_tracker.food_map[name.strip().title()] = calories
        
        monkeypatch.setattr(NutritionTracker, '__init__', mock_init)
        
        tracker = NutritionTracker()
        
        yield tracker
        
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        
        monkeypatch.setattr(NutritionTracker, '__init__', original_init)
    
    def test_calculate_calories(self, setup_environment):
        """Test 1: Test calorie calculation functionality"""
        tracker = setup_environment
        
        # Test calorie calculation for different foods
        apple_calories = tracker.calculate_calories("Apple", 150)  # 150g apple
        banana_calories = tracker.calculate_calories("Banana", 120)  # 120g banana
        chicken_calories = tracker.calculate_calories("Chicken Breast", 200)  # 200g chicken
        
        assert round(apple_calories, 2) == round(52 * 150 / 100, 2)
        assert round(banana_calories, 2) == round(89 * 120 / 100, 2)
        assert round(chicken_calories, 2) == round(165 * 200 / 100, 2)
        
        # Test non-existent food should return 0 calories
        unknown_calories = tracker.calculate_calories("Unknown Food", 100)
        assert unknown_calories == 0
        
        # Test case insensitivity
        apple_lowercase = tracker.calculate_calories("apple", 150)
        assert round(apple_lowercase, 2) == round(52 * 150 / 100, 2)
    
    def test_add_food_entry(self, setup_environment):
        """Test 2: Test adding food entry functionality"""
        tracker = setup_environment
        username = "test_user"
        
        # Add some food entries
        tracker.add_food_entry(username, "Apple", 150)
        tracker.add_food_entry(username, "Chicken Breast", 200)
        
        file_path = get_nutrition_data_path(username)
        assert os.path.exists(file_path)
        
        # Read CSV file and verify records
        df = pd.read_csv(file_path)
        assert len(df) == 2
        
        # Verify data correctness
        apple_entry = df[df['food'] == 'Apple'].iloc[0]
        chicken_entry = df[df['food'] == 'Chicken Breast'].iloc[0]
        
        assert float(apple_entry['grams']) == 150.0
        assert float(apple_entry['calories']) == round(52 * 150 / 100, 2)
        assert float(chicken_entry['grams']) == 200.0
        assert float(chicken_entry['calories']) == round(165 * 200 / 100, 2)
    
    def test_summarize_daily_nutrition(self, setup_environment):
        """Test 3: Test daily nutrition summary functionality"""
        tracker = setup_environment
        username = "test_user2"
        today = today_str()
        
        tracker.add_food_entry(username, "Apple", 150, today)
        tracker.add_food_entry(username, "Banana", 120, today)
        tracker.add_food_entry(username, "Chicken Breast", 200, today)
        
        tomorrow = "2025-05-03"
        tracker.add_food_entry(username, "Rice", 300, tomorrow)
        
        summary = tracker.summarize_daily_nutrition(username, today)
        
        expected_calories = (52 * 150 / 100) + (89 * 120 / 100) + (165 * 200 / 100)
        expected_calories = round(expected_calories, 2)
        
        # Verify total calories
        assert summary['calories'] == expected_calories
    
    def test_clear_today_nutrition(self, setup_environment):
        """Test 4: Test clearing today's nutrition records"""
        tracker = setup_environment
        username = "test_user3"
        today = today_str()
        yesterday = "2025-05-01"
        
        tracker.add_food_entry(username, "Apple", 150, today)
        tracker.add_food_entry(username, "Banana", 120, today)
        tracker.add_food_entry(username, "Rice", 300, yesterday)
        
        tracker.clear_today_nutrition(username)
        
        # Verify today's records were cleared
        file_path = get_nutrition_data_path(username)
        df = pd.read_csv(file_path)
        
        # Should only have yesterday's record left
        assert len(df) == 1
        assert df.iloc[0]['date'] == yesterday
        assert df.iloc[0]['food'] == "Rice"
    
    def test_get_today_entries(self, setup_environment):
        """Test 5: Test retrieving today's entries"""
        tracker = setup_environment
        username = "test_user4"
        today = today_str()
        yesterday = "2025-05-01"
        
        tracker.add_food_entry(username, "Apple", 150, today)
        tracker.add_food_entry(username, "Banana", 120, today)
        tracker.add_food_entry(username, "Rice", 300, yesterday)
        tracker.add_food_entry(username, "Broccoli", 200, yesterday)
        
        today_entries = tracker.get_today_entries(username)
        
        assert len(today_entries) == 2
        
        foods = [entry['food'] for entry in today_entries]
        assert "Apple" in foods
        assert "Banana" in foods
        assert "Rice" not in foods
        assert "Broccoli" not in foods