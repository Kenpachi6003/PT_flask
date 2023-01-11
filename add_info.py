from workout_functions import add_all_exercises
from flask_sqlalchemy import SQLAlchemy
from models import *
from info_to_insert import *
from starting_app import *


add_all_exercises(upper_chest_workouts[0], 'chest', 'upper chest')
add_all_exercises(mid_chest_workouts[0], 'chest', 'mid chest')
add_all_exercises(lower_chest_workouts[0], 'chest', 'lower chest')
add_all_exercises(workouts_for_back[0], 'back', None)
    