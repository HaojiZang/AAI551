# Author: Ruikang Li
# Date: 05/02/2025
# Description: Tests for the exercise tracking functionality

import os
import sys
import pytest
import pandas as pd
from datetime import datetime
import tempfile
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exercise import ExerciseTracker
from utils.helpers import today_str, get_exercise_data_path

class TestExerciseTracker:
    """Test class for ExerciseTracker functionality"""
    
    @pytest.fixture
    def setup_environment(self, monkeypatch):
        """Fixture to set up a test environment with mocked paths"""
        self.test_dir = tempfile.mkdtemp()
        
        tracker = ExerciseTracker()
        
        # save original reference file
        self.original_ref_file = tracker.reference_file
        
        # test reference file
        self.test_ref_file = os.path.join(self.test_dir, "exercise_dataset.csv")
        
        # sample reference data
        test_data = {
            "Activity, Exercise or Sport (1 hour)": ["Running", "Swimming", "Cycling", "Yoga", "HIIT"],
            "130 lb": [500, 400, 450, 200, 600],
            "155 lb": [600, 500, 550, 250, 700],
            "180 lb": [700, 600, 650, 300, 800],
            "205 lb": [800, 700, 750, 350, 900],
            "Calories per kg": [8.5, 7.0, 7.5, 4.0, 10.0]
        }
        pd.DataFrame(test_data).to_csv(self.test_ref_file, index=False)
        
        tracker.reference_file = self.test_ref_file
        
        def mock_get_exercise_data_path(username):
            return os.path.join(self.test_dir, f"{username}_exercise.csv")
        
        monkeypatch.setattr('utils.helpers.get_exercise_data_path', mock_get_exercise_data_path)
        
        def mock_ensure_data_file(username):
            os.makedirs(os.path.dirname(mock_get_exercise_data_path(username)), exist_ok=True)
        
        monkeypatch.setattr('utils.helpers.ensure_data_file', mock_ensure_data_file)
        
        yield tracker
        
        tracker.reference_file = self.original_ref_file
        shutil.rmtree(self.test_dir)
    
    def test_add_exercise_entry(self, setup_environment):
        """Test 1: Test adding an exercise entry to a user's log"""
        tracker = setup_environment
        username = "test_isolated_user"
        
        result = tracker.add_exercise_entry(username, "Running", 30, 300)
        
        assert result == True
        
        file_path = get_exercise_data_path(username)
        assert os.path.exists(file_path)
        
        df = pd.read_csv(file_path)
        assert len(df) == 1
        assert df.iloc[0]['activity'] == "Running"
        assert float(df.iloc[0]['duration']) == 30.0
        assert float(df.iloc[0]['calories']) == 300.0
        assert df.iloc[0]['date'] == today_str()
    
    def test_summarize_daily_exercise(self, setup_environment):
        """Test 2: Test summarizing daily exercise calories"""
        tracker = setup_environment
        username = "test_isolated_user_2"
        
        tracker.add_exercise_entry(username, "Running", 30, 300)
        tracker.add_exercise_entry(username, "Swimming", 45, 450)
        tracker.add_exercise_entry(username, "Cycling", 60, 500)
        
        total_calories = tracker.summarize_daily_exercise(username)
        
        assert total_calories == 1250.0
    
    def test_lookup_exercise_calories(self, setup_environment):
        """Test 3: Test looking up calories for a specific exercise"""
        tracker = setup_environment
        
        calories = tracker.lookup_exercise_calories("Running", 30)
        assert calories == 300.0
        
        calories = tracker.lookup_exercise_calories("Swimming", 45)
        assert calories == 375.0
    
    def test_get_exercise_options(self, setup_environment):
        """Test 4: Test retrieving exercise options from reference data"""
        tracker = setup_environment
        
        options = tracker.get_exercise_options()
        
        assert "Running" in options
        assert "Swimming" in options
        assert "Cycling" in options
        assert "Yoga" in options
        assert "HIIT" in options
        assert len(options) == 5
    
    def test_get_today_exercise_entries(self, setup_environment):
        """Test 5: Test retrieving today's exercise entries"""
        tracker = setup_environment
        username = "test_isolated_user_3"
        
        tracker.add_exercise_entry(username, "Running", 30, 300)
        tracker.add_exercise_entry(username, "Swimming", 45, 450)
        
        today_entries = tracker.get_today_exercise_entries(username)
        
        assert today_entries is not None
        assert len(today_entries) == 2
        
        activities = sorted(today_entries['activity'].tolist())
        assert activities[0] == "Running"
        assert activities[1] == "Swimming"
        
        running_entry = today_entries[today_entries['activity'] == "Running"].iloc[0]
        swimming_entry = today_entries[today_entries['activity'] == "Swimming"].iloc[0]
        
        # verify the values
        assert float(running_entry['duration']) == 30.0
        assert float(running_entry['calories']) == 300.0
        assert float(swimming_entry['duration']) == 45.0
        assert float(swimming_entry['calories']) == 450.0