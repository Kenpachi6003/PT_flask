from flask import Flask, redirect, render_template, request, flash, url_for, session
from flask_bcrypt import Bcrypt
import os

PT_flask = os.environ["PWD"]
import sys

sys.path.insert(0, PT_flask)
from datetime import timedelta
from app.models import (
    Workouts,
    WorkoutsView,
    User,
    UserView,
    Routine,
    RoutineView,
    Day_of_routine,
    DayView,
    Test_data,
    db,
    admin,
)
from app.info_to_insert import *
from app.workout_functions import (
    search,
    create_workout,
    remove_workout,
    workout_exists,
    list_of_videos,
)

from app.user_functions import user_exists, create_user


app = Flask(__name__)
app.secret_key = "lLIeYDuz9k4Ki4OIme-ff09SczH_Gtteol-n-BnwMIw"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ptraining.db"
# app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
admin.init_app(app)
admin.add_view(UserView(User, db.session))
admin.add_view(RoutineView(Routine, db.session))
admin.add_view(DayView(Day_of_routine, db.session))
admin.add_view(WorkoutsView(Workouts, db.session))

bcrypt = Bcrypt(app)
app.permanent_session_lifetime = timedelta(days=1)


@app.route("/workouts", methods=["GET", "POST"])
def workouts():
    if "user_id" in session:
        if request.method == "POST":
            searched = request.form["search"]
            exercises = search(searched, Workouts.query.all())
            return render_template("workouts.html", values=exercises)

        return render_template("workouts.html", values=Workouts.query.all())
    else:
        return redirect(url_for("login"))


@app.route("/add_workout", methods=["POST", "GET"])
def add_workout():
    if request.method == "POST":
        workout_name = request.form["workout_name"]
        body_part = request.form["body_part"]
        muscle_targeted = request.form["muscle_targeted"]
        workout = create_workout(workout_name, body_part, muscle_targeted)
        db.session.add(workout)
        db.session.commit()
        return redirect(url_for("workouts"))
    else:
        return render_template("add_workout.html")


@app.route("/delete_workout", methods=["GET", "POST"])
def delete_workout():
    if request.method == "POST":
        workout_name = request.form["workout_name"]

        if workout_exists(workout_name, Workouts.query.all()):
            workout = remove_workout(workout_name)
            db.session.delete(workout)
            db.session.commit()

        return redirect(url_for("workouts"))
    else:
        return render_template("delete_workout.html")


@app.route("/profile", methods=["POST", "GET"])
def profile():
    if "user_id" in session:
        if request.method == "POST":
            session["routine_day"] = request.form["routine_day"]
            return redirect(url_for("day"))
        else:
            return render_template("profile.html")
    else:
        return redirect(url_for("login"))


# new code
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/video")
def video():
    video_url = list_of_videos()
    return render_template("video.html", video_urls=video_url)


@app.route("/view")
def view():
    return render_template("view.html", values=Test_data.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
    if "user_id" in session:
        return redirect(url_for("profile"))
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]

        user = User.query.filter_by(username=username).first()

        if user is None:
            return redirect(url_for("create_account"))

        session["user_id"] = user.id

        flash("Login succesful!")

        return redirect(url_for("routine"))

    return render_template("login.html")


@app.route("/create_account", methods=["POST", "GET"])
def create_account():
    if "user_id" in session:
        return redirect(url_for("workouts"))
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]
        goal = request.form["goal"]

        if user_exists(User, username):
            flash("You already have an account")
            return redirect(url_for("login"))

        else:
            create_user(User, username, email, first_name, last_name, password, goal)
            flash("Account was created")
            return redirect(url_for("login"))
    return render_template("create_account.html")


@app.route("/logout")
def logout():
    if "user_id" in session:
        flash(f"You have been logged out!", "info")
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("email", None)
    return redirect(url_for("login"))


@app.route("/day")
def day():
    if "user_id" in session:
        routine_day = session["routine_day"]

        day_1 = which_day(session["user_id"], routine_day)

        return render_template(
            "day.html", routine_day=routine_day, values=day_1.workout_day()
        )


@app.route("/routine", methods=["POST", "GET"])
def routine():
    if "user_id" in session:
        routines = Routine.query.filter_by(id=2).first()

        return render_template("routine.html", routine_days=routines)
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        print("Creating database ", db)
        db.create_all()

        app.run(debug=True)
