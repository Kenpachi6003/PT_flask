from starting_app import app
from flask_sqlalchemy import SQLAlchemy
from models import db, Workouts, User, Test_data
from workout_functions import delete_workouts, delete_users


def main():
    delete_workouts(Workouts.query.all())
    db.session.commit()
    delete_users()


if __name__ == "__main__":
    with app.app_context():
        main()
