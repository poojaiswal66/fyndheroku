import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://hr:hr@127.0.0.1:1521/xe'
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

db = SQLAlchemy(app)
app.config['SECRET_KEY'] = os.urandom(24)


# class users(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(20), unique=False, nullable=False)
#     pswd = db.Column(db.String(200), unique=False, nullable=False)
#     radioname = db.Column(db.String(20), unique=False, nullable=False)
# db.create_all()

# class studentdata(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(20), unique=False, nullable=False)
#     email = db.Column(db.String(200), unique=False, nullable=False)
#     phone = db.Column(db.Integer(), unique=False, nullable=False)
#     address = db.Column(db.String(20), unique=False, nullable=False)
#     classname = db.Column(db.Integer(), unique=False, nullable=False)
# db.create_all()

# class fetchDb():
#     def fetchusers(user):
#         return users.query.filter_by(name=user).first()

# @login.user_loader
# def load_user():
#     return UserModel.query.get(int(id))
