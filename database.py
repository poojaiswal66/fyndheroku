import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:hr@localhost/Fynd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nvcvcmfwnbhaxl:1f811ffe2849a603a3b8f041a3dd96ef80e73edf687c546d12df037457c14bda@ec2-3-225-110-188.compute-1.amazonaws.com:5432/d5ugf03q0domg3'
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
