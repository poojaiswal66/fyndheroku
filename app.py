from routes.login import *
from routes.register import *
from routes.views import *

app.register_blueprint(blueprint, url_prefix='/login')
app.register_blueprint(blueprint_register, url_prefix='/register')
app.register_blueprint(views, url_prefix='/')

db.create_all()
@app.route('/logout')
def logout():
    msg = ""
    session.pop('user', None)
    msg = 'Logout Successful!'
    render_template('home.html', msg=msg)

if __name__ == '__main__':
    app.run(debug= True)
