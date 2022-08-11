from app import db


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
    marks = db.Column(db.Integer(), unique=False, nullable=False, default=0)
    total_fees_paid = db.Column(db.Integer(), unique=False, nullable=False, default=0)
    total_fees_due = db.Column(db.Integer(), unique=False, nullable=False, default=0)
    foreign_key = db.Column(db.Integer())
db.create_all()

class attendance(db.Model):
    index_attendance = db.Column(db.Integer(), primary_key = True)
    id = db.Column(db.Integer(), nullable=False)
    attendancestatus = db.Column(db.String(20), nullable=False)
    date_of_attendance = db.Column(db.String(20) , nullable=False)
db.create_all()