
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config['DEBUG'] = True

# Database setup
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="menster",
    password="1234-Hoedje-Van",
    hostname="menster.mysql.pythonanywhere-services.com",
    databasename="menster$comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Login Manager
app.secret_key = 'a verry verry secret 88 verry 77 secret kee'
login_manager = LoginManager()
login_manager.init_app(app)



# User Class #############################################

class User(UserMixin):
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


# Add Users ##################################################
all_users = {
        'admin': User('admin', generate_password_hash('secret')),
        'bob': User('bob', generate_password_hash('less-secret')),
        'Caroline': User('caroline', generate_password_hash('completelysecret')),
        'menster': User('menster', generate_password_hash('Harrie'))
    }

@login_manager.user_loader
def load_user(user_id):
    return all_users.get(user_id)



# Database Model #############################################

class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))



# Routes #####################################################

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('main_page.html', comments=Comment.query.all())

    else:
        comment = Comment(content=request.form['harrie'])
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('index'))



@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login_page.html', error=False)

    username = request.form['username']

    if username not in all_users:
        return render_template('login_page.html', error=True)

    # get the userobject from the lost
    user = all_users[username]

    if not user.check_password(request.form['password']):
        return render_template('login_page.html', error=True)


    return redirect(url_for('index'))


