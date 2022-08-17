from flask import session

from models import users


def getCurrentUser():
    user = None
    if 'user' in session:
        user = session.user
        user = users.query.filter_by(name=user).first()
    return user