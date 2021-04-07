from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user


app = Flask(__name__, template_folder='templates')

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/BROADBAND'
    app.config['SECRET_KEY'] = 'mysecret'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Connection(db.Model):
    __tablename__ = 'connection'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    location = db.Column(db.String(200))
    package = db.Column(db.Integer)
    address = db.Column(db.Text())

    def __init__(self, customer, location, package, address):
     self.customer = customer
     self.location = location
     self.package = package
     self.address = address



@app.route('/')
def index():
    return render_template('Broadband.html')


@app.route('/submit', methods=['POST','Get'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        location = request.form['location']
        package = request.form['package']
        address = request.form['address']
        #print(customer, location, package, address)
        if customer == '':
            return render_template('Broadband.html', message=
            'Please Enter Customer Name')

        if db.session.query(Connection).filter(Connection.customer == customer).count()== 0:
          data = Connection(customer, location, package, address)
          db.session.add(data)
          db.session.commit()
          return render_template('Confirmation.html')
        return render_template('Broadband.html', message=
            'you Already have SKY Broadband connection')

class MyModelView(ModelView):
    def is_accessible(self):
        return not current_user.is_authenticated  


admin = Admin(app)
admin.add_view(MyModelView(Connection, db.session))


@app.route('/login')
def login():
    connection= Connection.query.get(1)
    return 'Logged in!'

@app.route('/logout')
def logout():
    logout_user()
    return 'logged out'





if __name__ == '__main__':
    
    app.run(debug=True)