import os
from flask import Flask, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://hr:hr@127.0.0.1:1521/xe'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = os.urandom(24)

def get_current_user():
    user = None
    if 'user' in session:
        user = session.user
        user = users.query.filter_by(name=user).first()
    return user

class users(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    pswd = db.Column(db.String(200), unique=False, nullable=False)
    radioname = db.Column(db.String(20), unique=False, nullable=False)
db.create_all()

class studentdata(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(200), unique=False, nullable=False)
    phone = db.Column(db.Integer(), unique=False, nullable=False)
    address = db.Column(db.String(20), unique=False, nullable=False)
    classname = db.Column(db.String(20), unique=False, nullable=False)
db.create_all()

@app.route('/')
def index():
    user = get_current_user()
    return render_template('home.html', user=user)

@app.route('/login', methods = ['GET' , 'POST'])
def login():
    user = get_current_user()
    error = None
    htmlFile = 'login.html'
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('pswd')
        radioname = request.form.get('radioname')
        if radioname == 'Faculty':
            user = users.query.filter_by(name=name).first()
            if user:
                if check_password_hash(user.pswd, password):
                    session.user = user.name
                    htmlFile = "facultydashboard.html"
                else:
                    error = "Username or Password did not match, Please try again!"
            else:
                error = "Username or Password did not match, Please try again!"
        else:
            user = users.query.filter_by(name=name).first()
            if user:
                if check_password_hash(user.pswd, password):
                    session.user = user.name
                    htmlFile = "studentdashboard.html"
                else:
                    error = "Username or Password did not match, Please try again!"
            else:
                error = "Username or Password did not match, Please try again!"
    return render_template(htmlFile, loginerror=error, user=user)

@app.route('/register', methods=['GET','POST'])
def register():
    user = get_current_user()
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
    # user = get_current_user()
    # cursor = db.cursor()
    # cursor.execute("select * from studentdata")
    # data = cursor.fetchall()  # data from database
    return render_template('facultydashboard.html')

@app.route('/studentdashboard')
def studentdashboard():
    user = get_current_user()
    return render_template('studentdashboard.html', user=user)

@app.route('/addnewstudent', methods=['GET','POST'])
def addnewstudent():
    user = get_current_user()
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

@app.route('/singlestudent')
def singlestudent():
    user = get_current_user()
    return render_template('singlestudent.html', user=user)

@app.route('/updatestudent')
def updatestudent():
    user = get_current_user()
    return render_template('updatestudent.html', user=user)

@app.route('/logout')
def logout():

    msg = ""
    session.pop('user', None)
    msg = 'Logout Successful!'
    render_template('home.html')

if __name__ == '__main__':
    app.run(debug= True)
