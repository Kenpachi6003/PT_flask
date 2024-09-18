from app.starting_app import app
from app.user_functions import create_user
from app.workout_functions import (
    add_workouts_to_model,
    add_workouts_to_model,
    list_of_videos,
)
from app.models import Workouts, db, User
from info_to_insert import *


def main():

    create_user(
        User,
        "jcruz6003",
        "jcruz6003@gmail.com",
        "jose",
        "cruz",
        "loka1234",
        "build_muscle",
        "beginner",
        "admin",
        None,
    )
    create_user(
        User,
        "chris",
        "chris6003@gmail.com",
        "Christina",
        "Causey",
        "loka1234",
        "build_muscle",
        "advanced",
        None,
        1,
    )

    add_workouts_to_model(
        Workouts, upper_chest_workouts, "chest", "upper chest", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, mid_chest_workouts, "chest", "mid chest", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, lower_chest_workouts, "chest", "lower chest", list_of_videos()
    )
    add_workouts_to_model(Workouts, workouts_for_back, "back", None, list_of_videos())
    add_workouts_to_model(
        Workouts,
        front_delt_workouts + mid_delt_workouts + rear_delt_workouts,
        "shoulders",
        None,
        list_of_videos(),
    )
    add_workouts_to_model(
        Workouts, workouts_for_tricep, "arms", "triceps", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, workouts_for_bicep, "arms", "biceps", list_of_videos()
    )
    add_workouts_to_model(Workouts, workouts_for_legs, "legs", None, list_of_videos())
    add_workouts_to_model(
        Workouts, workouts_for_quads, "legs", "quads", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, workouts_for_hamstrings, "legs", "hamstrings", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, workouts_for_calves, "legs", "calves", list_of_videos()
    )


if __name__ == "__main__":
    with app.app_context():
        main()
