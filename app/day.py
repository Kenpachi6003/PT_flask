import os

PT_flask = os.environ["PWD"]
import sys

sys.path.insert(0, PT_flask)
from flask_sqlalchemy import SQLAlchemy
from app.models import db, Day_of_routine
from app.starting_app import app

routines = {
    "Free weight and cables": {
        "chest and triceps": [
            "incline barbell benchpress",
            "dumbell bench press",
            "decline barbell benchpress",
            "overhead tricep extension",
            "rope pulldown",
        ],
        "back and biceps": [
            "bentover barbell row",
            "bentover dumbell row",
            "seated row machine",
            "concentrated dumbell curls",
            "incline dumbell curl",
        ],
        "legs": [
            "leg press",
            "barbell squat",
            "frog pump",
            "hip abduction",
            "hip adduction",
        ],
        "shoulders and traps": [
            "standing straight bar overhead press",
            "dumbell lateral shoulder raises",
            "rear delt bent over flys",
            "shrugs",
            None,
        ],
    },
    "Machine focused": {
        "chest and triceps": [
            "incline chest press",
            "chest press",
            "machine flys",
            "dip machine",
            "tricep extension machine",
        ],
        "ack and biceps": [
            "lat pulldown machine",
            "seated row machine",
            "back extension machine",
            "bicep curl machine",
            "concentration curl machine",
        ],
        "legs": [
            "machine leg press",
            "leg press",
            "seated leg curl",
            "hip adduction",
            "hip abduction",
            "calf raise machine",
        ],
        "shoulders": [
            "machine shoulder press",
            "lateral shoulder raises",
            "reverse machine flys",
            "shrugs",
            None,
        ],
    },
}


def add_days_to_routine(model, routine, routine_name):

    for workout_day in routine:

        d = model(
            workout_day_name=workout_day,
            w1=routine[workout_day][0],
            w2=routine[workout_day][1],
            w3=routine[workout_day][2],
            w4=routine[workout_day][3],
            w5=routine[workout_day][4],
            routine_name=routine_name,
        )
        db.session.add(d)

    return d


def main():
    for routine in routines:

        added_day = add_days_to_routine(Day_of_routine, routines[routine], routine)
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        main()
