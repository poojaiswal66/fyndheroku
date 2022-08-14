import os
from flask import Flask, render_template, request, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from models import *
from database import *

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://hr:hr@127.0.0.1:1521/xe'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:hr@localhost/Fynd'
# db = SQLAlchemy(app)
# app.config['SECRET_KEY'] = os.urandom(24)

def getCurrentUser():
    user = None
    if 'user' in session:
        user = session.user
        user = users.query.filter_by(name=user).first()
    return user

db.create_all()

@app.route('/attendanceredir/<int:id>')
def attendanceredir(id):
    user = getCurrentUser()
    show_stud_data = studentdata.query.get(id)
    return render_template('markattendance.html', user=user, show_stud_data=show_stud_data)
@app.route('/markattendance', methods = ['GET' , 'POST'])
def markattendance():
    user = getCurrentUser()
    id = request.form.get('id')
    if request.method == 'POST':
        attendancestatus = request.form.get('attendancestatus')
        date_of_attendance = request.form.get('date_of_attendance')
        existingRecord = attendance.query.filter_by(id=id, date_of_attendance=date_of_attendance).first()
        if existingRecord:
            existingRecord.attendancestatus = attendancestatus
            db.session.commit()
        else:
            entry1 = attendance(id=int(request.form.get('id')), attendancestatus=attendancestatus, date_of_attendance=date_of_attendance)
            db.session.add(entry1)
            db.session.commit()
    users_data = studentdata.query.all()
    flash('Data Updated Successfully!')
    return render_template('facultydashboard.html', user=user, users_data=users_data)


@app.route('/')
def index():
    user = getCurrentUser()
    return render_template('home.html', user=user)

@app.route('/login', methods = ['GET' , 'POST'])
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
                    id = user.id
                    show_stud_data = studentdata.query.filter_by(foreign_key=id).all()
                    return render_template('studentdashboard.html', user=user, show_stud_data=show_stud_data)
                    # htmlFile = "studentdashboard.html"
                else:
                    error = "Username or Password did not match, Please try again!"
            else:
                error = "Username or Password did not match, Please try again!"

    return render_template(htmlFile, loginerror=error, user=user, users_data=users_data)

@app.route('/register', methods=['GET','POST'])
def register():
    user = getCurrentUser()
    if request.method == 'POST':
        'add entry to DB'
        name = request.form.get('name')
        password = request.form.get('pswd')
        hashed_password = generate_password_hash(password)
        radioname = request.form.get('radioname')

        user = users.query.filter_by(name=name).first()
        if user:
            # error = "User already exist"
            return render_template('register.html', registererror='User already exist')

        entry = users(name=name, pswd=hashed_password, radioname=radioname)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('index'))
        # msg = 'You have successfully registered!'
    return render_template('register.html', user=user)


@app.route('/facultydashboard', methods=['GET' , 'POST'])
def facultydashboard():
    user = getCurrentUser()
    radioname = request.form.get('radioname')
    if radioname == 'Faculty':
        users_data = studentdata.query.all()
        return render_template('facultydashboard.html', user=user, users_data=users_data)
    else:
        return redirect(url_for('login'))

@app.route('/studentdashboard')
def studentdashboard():
    user = getCurrentUser()
    # current_student_data = studentdata
    return render_template('studentdashboard.html', user=user)

@app.route('/addnewstudent', methods=['GET','POST'])
def addnewstudent():
    user = getCurrentUser()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        classname = request.form.get('classname')

        entry = studentdata(name=name, email=email, phone=phone, address=address, classname=classname)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('facultydashboard'))

    return render_template('addnewstudent.html', user=user)

@app.route('/singlestudent/<int:id>')
def singlestudent(id):
    user = getCurrentUser()
    show_stud_data = studentdata.query.get(id)
    return render_template('singlestudent.html', user=user, show_stud_data=show_stud_data)

# @app.route('/studentdashboard/<int:id>')
# def studentdashboard(id):
#     user = getCurrentUser()
#     show_data = studentdata.query.get(id)
#     return render_template('studentdashboard.html' , user=user, show_data=show_data)

@app.route('/fetchone/<int:id>')
def fetchone(id):
    user = getCurrentUser()
    show_stud_data = studentdata.query.get(id)
    return render_template('updatestudent.html', user=user, show_stud_data=show_stud_data)


@app.route('/updatestudent', methods = ['POST'])
def updatestudent():
    user = getCurrentUser()
    id = request.form.get('id')
    student = studentdata.query.filter_by(id=id).first()
    if request.method == 'POST':
        if student:
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            address = request.form.get('address')
            classname = request.form.get('classname')
            marks = request.form.get('marks')
            total_fees_paid = request.form.get('total_fees_paid')
            total_fees_due = request.form.get('total_fees_due')

            student = studentdata(
                name=name,
                email=email,
                phone=phone,
                address=address,
                classname=classname,
                id=id,
                marks=marks,
                total_fees_paid=total_fees_paid,
                total_fees_due=total_fees_due
            )
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('facultydashboard'))
        else:
            return
    return render_template('updatestudent.html', user=user)

@app.route('/deletestudent/<int:id>', methods=['GET','POST'])
def deletestudent(id):
    user = getCurrentUser()
    if request.method == 'GET':
        delete_stud = studentdata.query.filter_by(id=id).one()
        db.session.delete(delete_stud)
        db.session.commit()
        return redirect(url_for('facultydashboard'))
    return render_template('facultydashboard.html', user = user)

@app.route('/logout')
def logout():

    msg = ""
    session.pop('user', None)
    msg = 'Logout Successful!'
    render_template('home.html', msg)

if __name__ == '__main__':
    app.run(debug= True)
