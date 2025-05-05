from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_admin.contrib.sqla import ModelView
from flask import Flask, redirect, render_template, request, flash, url_for, session

db = SQLAlchemy()


class Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_name = db.Column(db.String, nullable=False)
    body_part = db.Column(db.String)
    muscle_targeted = db.Column(db.String, nullable=True)
    workout_link = db.Column(db.String, nullable=True)


class WorkoutsView(ModelView):
    column_list = ["id", "workout_name", "body_part", "muscle_targeted", "workout_link"]
    column_searchable_list = ["workout_name", "muscle_targeted"]
    form_columns = ["workout_name", "body_part", "muscle_targeted", "workout_link"]

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.workout_name.flags = {'required': True}
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        return form

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))

    def on_model_change(self, form, model, is_created):
        try:
            super().on_model_change(form, model, is_created)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating workout: {str(e)}", "error")


class Test_Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_name = db.Column(db.String, nullable=False)
    body_part = db.Column(db.String)
    muscle_targeted = db.Column(db.String, nullable=True)
    workout_link = db.Column(db.String, nullable=True)


class User(UserMixin, db.Model):
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
    routine_change_date = db.Column(db.Date, nullable=True)
    role = db.Column(db.String(50))
    level = db.Column(db.String)
    days_logged_in = db.Column(db.Integer)
    
    user_routine = db.Column(db.Integer, db.ForeignKey("routine.id"))


class UserView(ModelView):
    column_list = [
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "user_routine",
        "role",
        "level",
        "days_logged_in",
        "routine_change_date",
    ]
    
    form_columns = [
        "username",
        "email",
        "first_name",
        "last_name",
        "password",
        "role",
        "level",
        "user_routine",
        "days_logged_in",
        "routine_change_date"
    ]

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.password.flags = {'required': True}
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.password.flags = {'required': False}
        return form

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))

    def on_model_change(self, form, model, is_created):
        try:
            if is_created:
                model.password = form.password.data
            super().on_model_change(form, model, is_created)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating user: {str(e)}", "error")

    def on_model_delete(self, model):
        try:
            super().on_model_delete(model)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error deleting user: {str(e)}", "error")


class UserProgress(db.Model):
    __tablename__ = "user_progress"
    id = db.Column("id", db.Integer, primary_key=True)
    workout_done = db.Column(db.String)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight_lifted = db.Column(db.Integer)
    date = db.Column(db.Date)


class UserProgressView(ModelView):
    column_list = ["id", "sets"]
    form_columns = ["sets"]

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.sets.flags = {'required': True}
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        return form

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))

    def on_model_change(self, form, model, is_created):
        try:
            super().on_model_change(form, model, is_created)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating user progress: {str(e)}", "error")


class Test_User(db.Model):
    __tablename__ = "test_users"
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    goal = db.Column(db.String(20), nullable=True)
    beginning_day_id = db.Column(db.Integer, nullable=True)
    current_day_id = db.Column(db.Integer, nullable=True)
    routine_change_date = db.Column(db.Date, nullable=True)
    role = db.Column(db.String(50))
    level = db.Column(db.String, nullable=False)
    days_logged_in = db.Column(db.Integer)
    user_routine = db.Column(db.Integer, db.ForeignKey("routine.id"))


# each user will have their own routine set up to them
# here we will store our days for the routines


class Routine(db.Model):
    # routine could store just the day model
    __tablename__ = "routine"
    id = db.Column(db.Integer, primary_key=True)
    routine_name = db.Column(db.String)
    workouts = db.relationship("Day_of_routine", backref="routine")
    routine_level = db.Column(db.String, nullable=True)
    users_with_routine = db.relationship("User", backref="routine")


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
    w6 = db.Column(db.String, nullable=True)
    w7 = db.Column(db.String, nullable=True)
    w8 = db.Column(db.String, nullable=True)

    routine_name = db.Column(db.String, db.ForeignKey("routine.routine_name"))


class RoutineView(ModelView):
    column_list = [
        "id",
        "routine_name",
        "workouts",
        "routine_level",
        "users_with_routine",
    ]
    form_columns = ["routine_name", "routine_level"]

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.routine_name.flags = {'required': True}
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        return form

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))

    def on_model_change(self, form, model, is_created):
        try:
            super().on_model_change(form, model, is_created)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating routine: {str(e)}", "error")


class DayView(ModelView):
    column_list = [
        "id",
        "workout_day_name",
        "w1",
        "w2",
        "w3",
        "w4",
        "w5",
        "w6",
        "w7",
        "w8",
        "routine_name",
    ]
    form_columns = [
        "workout_day_name",
        "w1",
        "w2",
        "w3",
        "w4",
        "w5",
        "w6",
        "w7",
        "w8",
        "routine_name"
    ]

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.workout_day_name.flags = {'required': True}
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        return form

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))

    def on_model_change(self, form, model, is_created):
        try:
            super().on_model_change(form, model, is_created)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating day: {str(e)}", "error")


class Test_Day_of_routine(db.Model):

    # w stands for workout
    # Day could be the list of workouts that goes into Days
    id = db.Column(db.Integer, primary_key=True)
    workout_day_name = db.Column(db.String)
    w1 = db.Column(db.String)
    w2 = db.Column(db.String)
    w3 = db.Column(db.String)
    w4 = db.Column(db.String)
    w5 = db.Column(db.String, nullable=True)
    w6 = db.Column(db.String, nullable=True)
    w7 = db.Column(db.String, nullable=True)
    w8 = db.Column(db.String, nullable=True)

    routine_name = db.Column(db.String, db.ForeignKey("routine.routine_name"))


class Test_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_name = db.Column(db.String, nullable=False)
    body_part = db.Column(db.String)
    muscle_targeted = db.Column(db.String, nullable=True)


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("day"))  # Redirect non-admins to login


# Custom admin view
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("day"))
