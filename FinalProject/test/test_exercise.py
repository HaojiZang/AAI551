# Author: Ruikang Li
# Date: 04/11/2025

import os
import sys
import tkinter as tk
import pathlib

# Add parent directory to path to allow imports from parent directory
current_dir = pathlib.Path(__file__).parent.absolute()
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

def test_exercise_module():
    print("\n--- Testing exercise.py module ---")
    
    try:
        from exercise import lookup_exercise_calories, add_exercise_entry, summarize_daily_exercise
        
        # Test lookup_exercise_calories
        print("\nTesting lookup_exercise_calories function:")
        activities = ["Running, 5 mph (12 min/mile)", "Walking, 3 mph (20 min/mile)", "Cycling, moderate effort"]
        durations = [30, 45, 60]
        
        for activity in activities:
            for duration in durations:
                calories = lookup_exercise_calories(activity, duration)
                print(f"  {activity} for {duration} mins: {calories:.1f} calories")
        
        calories = lookup_exercise_calories("Dancing wildly", 30)
        print(f"  Dancing wildly for 30 mins: {calories:.1f} calories (should use fallback)")
        
        # Test add_exercise_entry
        print("\nTesting add_exercise_entry function:")
        test_user = "test_user"
        
        for activity, duration in zip(activities, durations):
            calories = lookup_exercise_calories(activity, duration)
            success = add_exercise_entry(test_user, activity, duration, calories)
            print(f"  Added '{activity}' for {duration} mins ({calories:.1f} cal): {'Success' if success else 'Failed'}")
        
        # Test summarize_daily_exercise
        print("\nTesting summarize_daily_exercise function:")
        daily_total = summarize_daily_exercise(test_user)
        print(f"  Total daily exercise calories: {daily_total:.1f}")
        
        return True
    
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Make sure you have the necessary Python files in the correct locations.")
        return False
    except Exception as e:
        print(f"Error during testing: {e}")
        return False

def test_exercise_ui():
    print("\n--- Testing exercise_ui.py module ---")
    
    try:
        root = tk.Tk()
        root.title("Exercise UI Test")
        
        print("Opening Exercise UI window...")
        print("Please interact with the UI to test its functionality:")
        print("1. Select an activity from the dropdown")
        print("2. Enter a duration in minutes")
        print("3. Click 'Calculate Calories'")
        print("4. Click 'Save Exercise'")
        print("5. Check if the exercise appears in the history")
        print("6. Try the 'Show Exercise Trends' button")
        print("7. Close the window when done testing")
        
        from exercise_ui import exercise_screen
        exercise_screen(root, "test_user")
        
        root.mainloop()
        return True
        
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Make sure you have the necessary Python files in the correct locations.")
        return False
    except Exception as e:
        print(f"Error during UI testing: {e}")
        return False

def test_visualization():
    print("\n--- Testing visualization module ---")
    
    try:
        from visualize import show_exercise_plot
        
        print("Opening visualization window...")
        print("If you've added exercise entries, you should see charts displaying:")
        print("1. Daily exercise calories")
        print("2. Activity distribution")
        
        show_exercise_plot("test_user")
        return True
        
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Make sure you have the necessary Python files in the correct locations.")
        return False
    except Exception as e:
        print(f"Error during visualization testing: {e}")
        return False

def test_data_reference():
    print("\n--- Testing data_reference.py module ---")
    
    try:
        from data_reference import load_exercise_reference
        
        print("Testing load_exercise_reference function:")
        exercise_data = load_exercise_reference()
        
        if not exercise_data:
            print("  No exercise data loaded.")
            return False
        
        print(f"  Successfully loaded {len(exercise_data)} exercise activities")
        
        # Print a few examples
        print("\nSample exercise data:")
        count = 0
        for activity, data in exercise_data.items():
            print(f"  {activity}: {data}")
            count += 1
            if count >= 3:
                break
        
        return True
        
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Make sure you have the necessary Python files in the correct locations.")
        return False
    except Exception as e:
        print(f"Error during data reference testing: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        if test_name == "module":
            test_exercise_module()
        elif test_name == "ui":
            test_exercise_ui()
        elif test_name == "viz":
            test_visualization()
        elif test_name == "data":
            test_data_reference()
        elif test_name == "all":
            module_success = test_exercise_module()
            data_success = test_data_reference()
            
            if module_success and data_success:
                ui_success = test_exercise_ui()
                if ui_success:
                    test_visualization()
    else:
        print("Available tests: module, ui, viz, data, all")
        print("Usage: python test/test_exercise.py [test_name]")
        print("\nExample: python test/test_exercise.py all")