from website.models import Test_data
from info_to_insert import *
from starting_app import app
from website.workout_functions import add_all_exercises


def main():
    add_all_exercises(Test_data, upper_chest_workouts[0], 'chest', 'upper chest')
    add_all_exercises(Test_data, mid_chest_workouts[0], 'chest', 'mid chest')
    add_all_exercises(Test_data, lower_chest_workouts[0], 'chest', 'lower chest')
    add_all_exercises(Test_data, workouts_for_back[0], 'back', None)
    add_all_exercises(Test_data, front_delt_workouts[0] + mid_delt_workouts[0] + rear_delt_workouts[0], 'shoulders', None)
    add_all_exercises(Test_data, workouts_for_tricep[0], 'arms', "triceps")
    add_all_exercises(Test_data, workouts_for_bicep[0], "arms", "biceps")
    add_all_exercises(Test_data, workouts_for_quads[0], "legs", "quads")
    add_all_exercises(Test_data, workouts_for_hamstrings[0], "legs", "hamstrings")
    add_all_exercises(Test_data, workouts_for_calves[0], "legs", "calves")
    



if __name__ == "__main__":
    with app.app_context():
        main()
