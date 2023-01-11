from flask_sqlalchemy import SQLAlchemy
from models import *
from info_to_insert import *
from starting_app import *


def delete_workouts():
    view_workouts= Workouts.query.all()

    for workout in view_workouts:
        db.session.delete(workout)

    return db.session.commit()


def add_all_exercises(exercises, body_part, muscle_targeted=None):
    view_workouts= Workouts.query.all()
    
    if exercises == str(exercises):
            if exercises not in view_workouts:
                workout = Workouts(
                    workout_name=exercises,
                    body_part=body_part,
                    muscle_targeted = muscle_targeted
            )
                db.session.add(workout)
    else:
        for exercise in exercises:
            if exercise not in view_workouts:
                workout = Workouts(
                    workout_name=exercise,
                    body_part=body_part,
                    muscle_targeted = muscle_targeted
            )
                db.session.add(workout)
                print(exercise)
    
    return db.session.commit()
