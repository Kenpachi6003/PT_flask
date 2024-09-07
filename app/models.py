from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()
admin = Admin()


class Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_name = db.Column(db.String, nullable=False)
    body_part = db.Column(db.String)
    muscle_targeted = db.Column(db.String, nullable=True)
    workout_link = db.Column(db.String, nullable=True)


class WorkoutsView(ModelView):
    column_list = ["id", "workout_name", "workout_link"]


class Test_Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_name = db.Column(db.String, nullable=False)
    body_part = db.Column(db.String)
    muscle_targeted = db.Column(db.String, nullable=True)
    workout_link = db.Column(db.String, nullable=True)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    goal = db.Column(db.String(20), nullable=True)
    beginning_day_id = db.Column(db.Integer, nullable=True)
    current_day_id = db.Column(db.Integer, nullable=True)
    user_routine = db.relationship("Routine", backref="user")


class UserView(ModelView):
    column_list = ["username", "email", "first_name", "last_name", "user_routine"]


class Test_User(db.Model):
    __tablename__ = "test_users"
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    goal = db.Column(db.String(20), nullable=True)


# each user will have their own routine set up to them
# here we will store our days for the routines


class Routine(db.Model):
    # routine could store just the day model
    __tablename__ = "routine"
    id = db.Column(db.Integer, primary_key=True)
    routine_name = db.Column(db.String)
    workouts = db.relationship("Day_of_routine", backref="routine")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class RoutineView(ModelView):
    column_list = ["id", "routine_name", "workouts", "user_id"]


class Day_of_routine(db.Model):

    # w stands for workout
    # Day could be the list of workouts that goes into Days
    id = db.Column(db.Integer, primary_key=True)
    workout_day_name = db.Column(db.String)
    w1 = db.Column(db.String)
    w2 = db.Column(db.String)
    w3 = db.Column(db.String)
    w4 = db.Column(db.String)
    w5 = db.Column(db.String, nullable=True)

    routine_name = db.Column(db.String, db.ForeignKey("routine.routine_name"))


class DayView(ModelView):
    column_list = [
        "id",
        "workout_day_name",
        "w1",
        "w2",
        "w3",
        "w4",
        "w5",
        "routine_name",
    ]


class Test_Day(db.Model):
    # w stands for workout
    id = db.Column(db.Integer, primary_key=True)
    workout_day_name = db.Column(db.String, nullable=False)
    w1 = db.Column(db.String)
    w2 = db.Column(db.String)
    w3 = db.Column(db.String)
    w4 = db.Column(db.String)
    w5 = db.Column(db.String)


class Test_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_name = db.Column(db.String, nullable=False)
    body_part = db.Column(db.String)
    muscle_targeted = db.Column(db.String, nullable=True)
