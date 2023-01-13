from flask import Flask, redirect, render_template, request, flash, url_for, session
from flask_bcrypt import Bcrypt
from datetime import timedelta
from models import Workouts, User, db
from info_to_insert import *
from workout_functions import search, create_workout, user_exists, create_user, remove_workout, workout_exists
from routines import chest_day, back_day



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
    if "user_id" in session:
        if request.method == "POST":
            searched = request.form["search"]
            exercises = search(searched)
            return render_template("workouts.html", values=exercises)

        return render_template('workouts.html', values=Workouts.query.all())
    else:
        return redirect(url_for("login"))


@app.route("/add_workout", methods=['POST', 'GET'])
def add_workout():
    if request.method =="POST":
        workout_name = request.form['workout_name']
        body_part = request.form['body_part']
        muscle_targeted = request.form['muscle_targeted']
        create_workout(workout_name, body_part, muscle_targeted)
        return redirect(url_for("workouts"))
    else:
        return render_template("add_workout.html")

@app.route("/delete_workout", methods=["GET", "POST"])
def delete_workout():
    if request.method == "POST":
        workout_name = request.form["workout_name"]

        if workout_exists(workout_name):
            remove_workout(workout_name)


        return redirect(url_for("workouts"))
    else:
        return render_template("delete_workout.html")


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
    if "user_id" in session:
        return redirect(url_for("workouts"))
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
    if "user_id" in session:
        return redirect(url_for("workouts"))
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        name = request.form["name"]
        password = request.form['password']
        goal = request.form['goal']

        if user_exists(username):  
            flash("You already have an account")
            return redirect(url_for("login"))

        else:
            create_user(username, email, name, password, goal)
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

   
        
        return render_template("day.html", day_1=chest_day(session["user_id"]), day_2=back_day(session["user_id"]))

if __name__ == "__main__":
    with app.app_context():
        print("Creating database ", db)
        db.create_all()

        app.run(debug=True)
