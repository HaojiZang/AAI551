# Exercise Tracker Module

This module tracks exercises, calculates calories burned, and visualizes exercise trends.

## Testing

Run the tests from the project root directory:

```bash
# Create sample data
python test/create_sample_data.py

# Run all tests
python test/test_exercise.py all

# Or run specific tests
python test/test_exercise.py module  # Core functions
python test/test_exercise.py ui      # User interface
python test/test_exercise.py viz     # Visualizations
python test/test_exercise.py data    # Reference data

Using the UI

Select an activity from the dropdown
Enter duration in minutes
Calculate calories by clicking the button
Save the exercise to log it
View trends with the "Show Exercise Trends" button

Keyboard Navigation

Tab: Move between fields
Enter: Move to next field or activate buttons
Activity field → Duration → Calculate → Save
