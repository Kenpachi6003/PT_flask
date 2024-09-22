from faker import Faker

fake = Faker()

from faker.providers import BaseProvider


class Workout_data(BaseProvider):
    def workout_name(self):
        return "lat pulldown"

    def body_part(self):
        return "back"

    def muscle_targeted(self):
        return None


fake.add_provider(Workout_data)


class Day_data(BaseProvider):

    routine_name = "Free weight and cables"

    workout_day_name = "chest and triceps"
    w1 = "incline barbell benchpress"
    w2 = "dumbell bench press"

    w3 = "decline barbell benchpress"

    w4 = "overhead tricep extension"

    w5 = "rope pulldown"


fake.add_provider(Day_data)
