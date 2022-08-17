from flask import Blueprint
from flask import request, session, render_template
from werkzeug.security import check_password_hash

from currentuser import getCurrentUser
from models import *

blueprint = Blueprint("login", __name__, static_folder="static", template_folder="template")

@blueprint.route('/login', methods = ['GET' , 'POST'])
def login():
    user = getCurrentUser()
    error = None
    htmlFile = 'login.html'
    users_data = None
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('pswd')
        radioname = request.form.get('radioname')
        loginUserData = users.query.filter_by(name = name, radioname = radioname).first()
        if loginUserData == None:
            error = 'Invalid Credential'


        if loginUserData and radioname == "Faculty":
            user =loginUserData
            if user:
                if check_password_hash(user.pswd, password):
                    session.user = user.name
                    users_data = studentdata.query.all()
                    htmlFile = "facultydashboard.html"
                else:
                    error = "Username or Password did not match, Please try again!"
            else:
                error = "Username or Password did not match, Please try again!"
        if loginUserData and radioname == "Student":
            user = loginUserData
            if user:
                if check_password_hash(user.pswd, password):
                    session.user = user.name
                    show_stud_data = studentdata.query.filter_by(email=name).all()
                    return render_template('studentdashboard.html', user=user, show_stud_data=show_stud_data)
                else:
                    error = "Username or Password did not match, Please try again!"
            else:
                error = "Username or Password did not match, Please try again!"

    return render_template(htmlFile, loginerror=error, user=user, users_data=users_data)