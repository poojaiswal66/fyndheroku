from flask import render_template, request, url_for, flash, Blueprint
from werkzeug.utils import redirect
from currentuser import getCurrentUser
from models import *

views = Blueprint("views", __name__, static_folder="static", template_folder="template")

@views.route('/attendanceredir/<int:id>')
def attendanceredir(id):
    user = getCurrentUser()
    show_stud_data = studentdata.query.get(id)
    return render_template('markattendance.html', user=user, show_stud_data=show_stud_data)

@views.route('/markattendance', methods = ['GET' , 'POST'])
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

@views.route('/')
def index():
    user = getCurrentUser()
    return render_template('home.html', user=user)

@views.route('/facultydashboard', methods=['GET' , 'POST'])
def facultydashboard():
    user = getCurrentUser()
    radioname = request.form.get('radioname')
    if radioname == 'Faculty':
        users_data = studentdata.query.all()
        return render_template('facultydashboard.html', user=user, users_data=users_data)
    else:
        return redirect(url_for('login.login'))

@views.route('/studentdashboard')
def studentdashboard():
    user = getCurrentUser()
    return render_template('studentdashboard.html', user=user)

@views.route('/addnewstudent', methods=['GET','POST'])
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
        return showStudDataFacDashboard(user)

    return render_template('addnewstudent.html', user=user)

@views.route('/singlestudent/<int:id>')
def singlestudent(id):
    user = getCurrentUser()
    show_stud_data = studentdata.query.get(id)
    return render_template('singlestudent.html', user=user, show_stud_data=show_stud_data)

# @app.route('/studentdashboard/<int:id>')
# def studentdashboard(id):
#     user = getCurrentUser()
#     show_data = studentdata.query.get(id)
#     return render_template('studentdashboard.html' , user=user, show_data=show_data)

@views.route('/fetchone/<int:id>')
def fetchone(id):
    user = getCurrentUser()
    show_stud_data = studentdata.query.get(id)
    return render_template('updatestudent.html', user=user, show_stud_data=show_stud_data)

@views.route('/updatestudent', methods = ['POST'])
def updatestudent():
    user = getCurrentUser()
    id = request.form.get('id')
    existing_data = studentdata.query.filter_by(id=id).first()
    if request.method == 'POST':
        if existing_data:
            existing_data.name = request.form.get('name')
            existing_data.email = request.form.get('email')
            existing_data.phone = request.form.get('phone')
            existing_data.address = request.form.get('address')
            existing_data.classname = request.form.get('classname')
            existing_data.marks = request.form.get('marks')
            existing_data.total_fees_paid = request.form.get('total_fees_paid')
            existing_data.total_fees_due = request.form.get('total_fees_due')
            db.session.commit()
            return showStudDataFacDashboard(user)
        else:
            return
    return render_template('updatestudent.html', user=user)

@views.route('/deletestudent/<int:id>', methods=['GET','POST'])
def deletestudent(id):
    user = getCurrentUser()
    if request.method == 'GET':
        delete_stud = studentdata.query.filter_by(id=id).one()
        db.session.delete(delete_stud)
        db.session.commit()
        return showStudDataFacDashboard(user)
    return render_template('facultydashboard.html', user = user)

def showStudDataFacDashboard(user):
    users_data = studentdata.query.all()
    return render_template('facultydashboard.html', user=user, users_data=users_data)