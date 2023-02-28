from faker import Faker

fake = Faker()

from faker.providers import BaseProvider

class Workout_data(BaseProvider):
    def workout_name(self):
        return 'lat pulldown'

    def body_part(self):
        return 'back'

    def muscle_targeted(self):
        return None

fake.add_provider(Workout_data)

