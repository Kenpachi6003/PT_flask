import pytest
import os

PT_flask = os.environ["PWD"]
import sys

sys.path.insert(0, PT_flask)

from app.workout_functions import (
    create_workout,
    workout_exists,
    remove_workout,
    search,
    delete_workouts,
    filter_video_name,
    video_to_add_to_model,
)
from app.starting_app import app
from app.models import db, Test_Workouts
from testing_data import fake


class Test_Workout_Functions:
    def test_create_workout(self):
        with app.app_context():
            workout = create_workout(
                fake.workout_name(),
                fake.body_part(),
                fake.muscle_targeted(),
                Test_Workouts,
            )

            assert (
                workout.workout_name,
                workout.body_part,
                workout.muscle_targeted,
            ) == (
                "lat pulldown",
                "back",
                None,
            )

    def test_workout_exists(self):
        with app.app_context():
            assert workout_exists(fake.workout_name(), Test_Workouts) == True
            assert workout_exists("test", Test_Workouts) == False

    def test_search(self):
        with app.app_context():
            assert search(fake.workout_name(), Test_Workouts) == [
                Test_Workouts.query.filter_by(workout_name="lat pulldown").first()
            ]

    def test_remove_workout(self):
        with app.app_context():
            assert (
                remove_workout(fake.workout_name(), Test_Workouts)
                == Test_Workouts.query.filter_by(workout_name="lat pulldown").first()
            )

    def test_filter_video_name(self):

        assert (
            filter_video_name(
                "https://causey.s3.us-east-2.amazonaws.com/workout_vids/incline_barbell_benchpress.mov"
            )
            == "incline_barbell_benchpress"
        )

    def test_video_to_add_to_model(self):
        assert (
            video_to_add_to_model(
                "incline_barbell_benchpress",
                [
                    "https://causey.s3.us-east-2.amazonaws.com/workout_vids/incline_barbell_benchpress.mov",
                    "https://causey.s3.us-east-2.amazonaws.com/workout_vids/incline_dumbell_press.mov",
                    "https://causey.s3.us-east-2.amazonaws.com/workout_vids/dumbell_bench_press.mov",
                ],
            )
            == "https://causey.s3.us-east-2.amazonaws.com/workout_vids/incline_barbell_benchpress.mov"
        )
