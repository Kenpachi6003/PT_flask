import os

PT_flask = os.environ["PWD"]
import sys

sys.path.insert(0, PT_flask)
from flask_sqlalchemy import SQLAlchemy
from app.models import db, Day_of_routine, Routine
from app.starting_app import app
from app.day import routines


def make_routine_name(model, routine_name):

    routine = model(routine_name=routine_name)
    return routine


def main():
    for routine in routines:

        routine_name = make_routine_name(Routine, routine)
        db.session.add(routine_name)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        main()
