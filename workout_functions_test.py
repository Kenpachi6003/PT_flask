import pytest
from workout_functions import add_all_exercises
from starting_app import app
from models import Workouts


def test_add_all_workouts():
    with app.app_context():
        workout_name = "example workout"

        add_all_exercises(workout_name, 'any', None)
        
        workout = Workouts.query.filter_by(body_part='any')

        assert workout_name in workout
