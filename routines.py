from flask_sqlalchemy import SQLAlchemy
from models import *


class Day:
    def __init__(self, user_id, workout_1, workout_2, workout_3, workout_4=None):
        self.user_id = user_id
        self.workout_1 = workout_1
        self.workout_2 = workout_2
        self.workout_3 = workout_3
        self.workout_4 = workout_4



    def workout_day(self):
        user = User.query.filter_by(id=self.user_id).first()
        workouts = Workouts.query.all()
        workout_day = []

        workouts_given = [self.workout_1, self.workout_2, self.workout_3, self.workout_4]

        if user.goal == "build_muscle":
            for workout in workouts:
                if workout.workout_name in workouts_given:
                    workout_day.append(workout)



        return workout_day

    
def which_day(user_id, day):
    #a function that returns the day i am using
    chosen_day = ""
    day_1 = Day(user_id, "incline barbell chest press", "flat barbell bench press", "decline barbell bench press", "push-up")
    day_2 = Day(user_id, "lat pulldown", "seated cable rows", "back extensions", "pull up")
    day_3 = Day(user_id, "hack squat", "leg press" , "leg extensions", "seated leg curl")
    day_4 = Day(user_id, "arnold press", "lateral shoulder raise", "reverse flyes", )

    if day == "Chest":
        chosen_day = day_1
    elif day == "Back":
        chosen_day = day_2
    elif day == "Legs":
        chosen_day = day_3
    elif day == "Shoulders":
        chosen_day = day_4

    return chosen_day