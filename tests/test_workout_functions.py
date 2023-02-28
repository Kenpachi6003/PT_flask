import pytest
import os
PT_flask = os.environ['PWD']
import sys 
sys.path.insert(0, PT_flask)

from workout_functions import (
    create_workout,
    workout_exists,
    remove_workout,
    search,
    delete_workouts,
)
from starting_app import app
from models import db, Test_data
from testing_data import fake



class Test_Workout_Functions:
    def test_create_workout(self):
        workout = create_workout(
            fake.workout_name(), fake.body_part(), fake.muscle_targeted(), Test_data
        )

        assert (workout.workout_name, workout.body_part, workout.muscle_targeted) == (
            "lat pulldown",
            "back",
            None,
        )

    def test_workout_exists(self):
        with app.app_context():
            assert workout_exists(fake.workout_name(), Test_data.query.all()) == True
            assert workout_exists("test", Test_data.query.all()) == False

    def test_remove_workout(self):
        with app.app_context():
            assert (
                remove_workout(fake.workout_name(), Test_data)
                == Test_data.query.filter_by(workout_name="lat pulldown").first()
            )

    def test_search(self):
        with app.app_context():
            assert search(fake.workout_name(), Test_data) == [
                Test_data.query.filter_by(workout_name="lat pulldown").first()
            ]
