import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:hr@localhost/Fynd'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nvcvcmfwnbhaxl:1f811ffe2849a603a3b8f041a3dd96ef80e73edf687c546d12df037457c14bda@ec2-3-225-110-188.compute-1.amazonaws.com:5432/d5ugf03q0domg3'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = os.urandom(24)






