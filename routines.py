from flask_sqlalchemy import SQLAlchemy
from models import *

def chest_day(user_id):
    user = User.query.filter_by(id=user_id).first()
    workouts = Workouts.query.all()
    chest_day = []

    if user.goal == "build_muscle":
        for workout in workouts:
            if workout.workout_name == "incline barbell chest press":
                chest_day.append(workout)
            elif workout.workout_name == "flat barbell bench press":
                chest_day.append(workout)
            elif workout.workout_name == "decline barbell bench press":
                chest_day.append(workout)
            elif workout.workout_name == "push-up":
                chest_day.append(workout)
            
            

    return chest_day


def back_day(user_id):
    user = User.query.filter_by(id=user_id).first()
    workouts = Workouts.query.all()
    back_day = []

    if user.goal == "build_muscle":
        for workout in workouts:
            if workout.workout_name == "seated cable rows":
                back_day.append(workout)
            elif workout.workout_name == "lat pulldown":
                back_day.append(workout)
            elif workout.workout_name == "back extensions":
                back_day.append(workout)
            elif workout.workout_name == "pull up":
                back_day.append(workout)
            
            

    return back_day