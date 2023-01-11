from flask_sqlalchemy import SQLAlchemy
from models import *
from info_to_insert import *



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


def search(searched):
    workouts = Workouts.query.all()
    exercises = []

    for exercise in workouts:
        if searched in exercise.workout_name:
            exercises.append(exercise)
        elif searched in exercise.body_part:
            exercises.append(exercise)

    return exercises

def workout_exists(workout_name):
    workouts = Workouts.query.all()

    for workout in workouts:
        if workout_name == workout.workout_name:
            return True
    return False

def create_workout(workout_name, body_part, muscle_targeted):
    workout = Workouts(workout_name=workout_name, body_part=body_part, muscle_targeted=muscle_targeted)
    db.session.add(workout)
    db.session.commit()
    return workout

def remove_workout(workout_name):
    workout = Workouts.query.filter_by(workout_name=workout_name).first()
    db.session.delete(workout)
    return db.session.commit()
        

def user_exists(username):
    users = User.query.all()

    for account in users:
        if username == account.username:
            return True
    return False

def create_user(username, email, name, password):
    user = User(username=username, email=email, name=name, password=password )
    db.session.add(user)
    db.session.commit()
    return user