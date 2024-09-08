from flask import Flask, redirect, render_template, request, flash, url_for, session
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
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
    Admin,
    AdminView,
    MyAdminIndexView,
)
from app.info_to_insert import *
from app.workout_functions import (
    search,
    create_workout,
    remove_workout,
    workout_exists,
    list_of_videos,
    routine_with_videos,
    add_links_to_routine_days,
    filter_video_name,
)

from app.user_functions import user_exists, create_user

app = Flask(__name__)
admin = Admin(app, index_view=MyAdminIndexView())

app.secret_key = "lLIeYDuz9k4Ki4OIme-ff09SczH_Gtteol-n-BnwMIw"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ptraining.db"
# app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

admin.add_view(UserView(User, db.session))
admin.add_view(RoutineView(Routine, db.session))
admin.add_view(DayView(Day_of_routine, db.session))
admin.add_view(WorkoutsView(Workouts, db.session))
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
app.permanent_session_lifetime = timedelta(days=1)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# new code


@app.route("/video")
def video():
    video_url = list_of_videos()
    return render_template("video.html", video_urls=video_url)


@app.route("/play")
def play_video():
    video_url = request.args.get("video_url")  # Get the video URL from query parameter

    return render_template(
        "play_video.html",
        video_url=video_url,
        workout_name=filter_video_name(video_url),
    )


@app.route("/", methods=["POST", "GET"])
def login():
    if "user_id" in session:
        return redirect(url_for("day"))
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session["user_id"] = user.id

            login_user(user)

            if user.role == None:
                routine = Routine.query.filter_by(id=user.user_routine).first()

                session["beginning_day"] = routine.workouts[0].id

                flash("Login succesful!")
                return redirect(url_for("day"))
            return redirect(url_for("admin.index"))
        elif user is None:
            return redirect(url_for("create_account"))

    return render_template("login.html")


@app.route("/create_account", methods=["POST", "GET"])
def create_account():
    if "user_id" in session:
        return redirect(url_for("day"))
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


@app.route("/about_me")
def about_me():
    return render_template("about_me.html")


@app.route("/routine", methods=["POST", "GET"])
def routine():
    if "user_id" in session:
        routines = Routine.query.filter_by(id=1).first()

        routines1 = routine_with_videos(routines, Workouts.query.all())
        # breakpoint()
        return render_template("routine.html", routine_days=routines1)
    else:
        return redirect(url_for("login"))


@app.route("/day", methods=["POST", "GET"])
def day():
    if "user_id" in session:
        user = User.query.filter_by(id=session["user_id"]).first()

        if user.current_day_id == None:
            user.current_day_id = session["beginning_day"]
            db.session.commit()

        day = Day_of_routine.query.filter_by(id=user.current_day_id).first()
        workout_day = add_links_to_routine_days(day, Workouts.query.all())

        return render_template(
            "day.html", workout_day=workout_day, day=day.workout_day_name
        )
    else:
        return redirect(url_for("login"))


@app.route("/change_day_id", methods=["POST", "GET"])
def change_day_id():

    user = User.query.filter_by(id=session["user_id"]).first()
    routine = Routine.query.filter_by(id=user.user_routine).first()

    if user.current_day_id >= routine.workouts[0].id + 3:
        user.current_day_id = session["beginning_day"]
    else:
        user.current_day_id = user.current_day_id + 1

    db.session.commit()

    return redirect(url_for("day"))


if __name__ == "__main__":
    with app.app_context():
        print("Creating database ", db)
        db.create_all()

        app.run(debug=True)
