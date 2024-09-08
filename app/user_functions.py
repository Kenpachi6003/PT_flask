from flask_sqlalchemy import SQLAlchemy
from app.models import User, db


def user_exists(model, username):
    users = model.query.all()

    for account in users:

        if username == account.username:
            return True

    return False


def create_user(
    model, username, email, first_name, last_name, password, goal, role=None
):
    user = model(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,
        goal=goal,
        role=role,
    )
    db.session.add(user)
    db.session.commit()
    return user


def delete_users(model):
    view_users = model.query.all()
    for user in view_users:
        db.session.delete(user)
    return db.session.commit()
