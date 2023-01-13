from starting_app import app
from workout_functions import delete_workouts, delete_users

def main():
    delete_workouts()
    delete_users()


if __name__ == "__main__":
    with app.app_context():
        main()
