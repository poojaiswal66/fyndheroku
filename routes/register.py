from flask import request, render_template, url_for, Blueprint
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect
from currentuser import getCurrentUser
from models import *

blueprint_register  = Blueprint("register", __name__, static_folder="static", template_folder="template")

@blueprint_register.route('/register', methods=['GET','POST'])
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
        return redirect(url_for('views.index'))
        # msg = 'You have successfully registered!'
    return render_template('register.html', user=user)