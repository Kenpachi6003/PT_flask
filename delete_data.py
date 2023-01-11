from starting_app import app
from workout_functions import delete_workouts

def main():
    delete_workouts()


if __name__ == "__main__":
    with app.app_context():
        main()
