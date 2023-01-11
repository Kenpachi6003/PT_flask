from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_name = db.Column(db.String, nullable=False)
    body_part = db.Column(db.String)
    muscle_targeted = db.Column(db.String, nullable=True)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    name = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=False)
