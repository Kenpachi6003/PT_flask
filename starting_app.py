from flask import Flask, redirect, render_template, request, flash, url_for, session
from flask_bcrypt import Bcrypt
from datetime import timedelta
from models import Workouts, User, db
from info_to_insert import *



app = Flask(__name__)
app.secret_key = "lLIeYDuz9k4Ki4OIme-ff09SczH_Gtteol-n-BnwMIw"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ptraining.db"
#app.config["SQLALCHEMY_ECHO"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
 
bcrypt = Bcrypt(app)
app.permanent_session_lifetime = timedelta(days=1)


@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
    exercises = []
    if "user_id" in session:
        if request.method == "POST":
            searched = request.form["search"]
            exercise_list = Workouts.query.all()

            for exercise in exercise_list:

                if searched == exercise.workout_name:
                    exercises.append(exercise)
                    return render_template("workouts.html", values=exercises)
                elif searched == exercise.body_part:
                    exercises.append(exercise)
            return render_template("workouts.html", values = exercises)


        return render_template('workouts.html', values=Workouts.query.all())
    else:
        return redirect(url_for("login"))

@app.route("/add_workout", methods=['POST', 'GET'])
def add_workout():

    if request.method =="POST":
        workout_name = request.form['workout_name']
        body_part = request.form['body_part']
        muscle_targeted = request.form['muscle_targeted']
        
        workout = Workouts(workout_name=workout_name, body_part=body_part, muscle_targeted=muscle_targeted)
        db.session.add(workout)
        db.session.commit()
        return redirect(url_for("workouts"))
    else:
        return render_template("add_workout.html")

@app.route('/routines')
def routines():
    if "user_id" in session:
        return render_template('routines.html', values=Workouts.query.filter_by(body_part='back'))
    else:
        return redirect(url_for("login"))

#new code
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view")
def view():
    
    return render_template("view.html", values=User.query.all())

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]
        
        user = User.query.filter_by(username=username).first()

        if user is None:
            return redirect(url_for("create_account"))
        
        session["user_id"] = user.id

        flash("Login succesful!")

        return redirect(url_for("workouts"))

    return render_template("login.html")
        
    

@app.route("/create_account", methods=["POST", "GET"])
def create_account():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        name = request.form["name"]
        password = request.form['password']
        users = User.query.all()

        for account in users:
            if username == account.username:
               
                flash("You already have an account")
                return redirect(url_for("login"))


        user = User(username=username, email=email, name=name, password=password )
        db.session.add(user)
        db.session.commit()

        flash("email was saved")

        return redirect(url_for("login"))
    return render_template("create_account.html")


def logged_in(user):
    return user is not None 

@app.route("/logout")
def logout():
    if "user_id" in session:
        
        flash(f"You have been logged out!", "info")
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        print("Creating database ", db)
        db.create_all()
        # workout = Workouts(workout_name="Push Ups")
        # db.session.add(workout)
        # db.session.commit()

        app.run(debug=True)

