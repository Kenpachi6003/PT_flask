from flask_sqlalchemy import SQLAlchemy
import boto3
from app.models import Workouts, db
from app.info_to_insert import *

s3 = boto3.client("s3")
bucket_name = "causey"


def delete_workouts():
    view_workouts = Workouts.query.all()

    for workout in view_workouts:
        db.session.delete(workout)

    return db.session.commit()


def list_of_videos():
    # retrive objects in bucket list
    response = s3.list_objects_v2(Bucket=bucket_name)

    # extracts image urls
    video_urls = []
    videos = []

    if "Contents" in response:
        video_index = 0
        for obj in response["Contents"]:

            video_urls.append(
                s3.generate_presigned_url(
                    "get_object", Params={"Bucket": bucket_name, "Key": obj["Key"]}
                )
            )
            video_url_only = video_urls[video_index].split("?")
            videos.append(video_url_only[0])
            video_index += 1

    return videos


def filter_video_name(video_name):
    delimiters = ["https://causey.s3.us-east-2.amazonaws.com/workout_vids/", ".mov"]
    for delimiter in delimiters:
        if delimiter in video_name:
            video_name = "".join(video_name.split(delimiter))

    return video_name


def video_to_add_to_model(workout_name, videos):
    video_name = ""

    for video in videos:

        if workout_name == filter_video_name(video):
            video_name = video

    return video_name


def add_workouts_to_model(model, workout_names, body_part, muscle_targeted, videos):
    for workout_name in workout_names:
        workout = model(
            workout_name=workout_name,
            body_part=body_part,
            muscle_targeted=muscle_targeted,
            workout_link=video_to_add_to_model(workout_name, list_of_videos()),
        )

        db.session.add(workout)
    return db.session.commit()


def search(searched, model):
    workouts = model.query.all()
    exercises = []

    for exercise in workouts:
        if searched in exercise.workout_name:
            exercises.append(exercise)
        elif searched in exercise.body_part:
            exercises.append(exercise)

    return exercises


def workout_exists(workout_name, model):
    workouts = model.query.all()

    for workout in workouts:
        if workout_name == workout.workout_name:
            return True
    return False


def create_workout(workout_name, body_part, muscle_targeted, model):
    workout = model(
        workout_name=workout_name, body_part=body_part, muscle_targeted=muscle_targeted
    )
    db.session.add(workout)
    db.session.commit()
    return workout


def remove_workout(workout_name, model):
    workout = model.query.filter_by(workout_name=workout_name).first()
    db.session.delete(workout)
    return db.session.commit()
