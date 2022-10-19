import os
from flask import Flask
from flask_login import LoginManager, current_user
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import timedelta
from App.controllers.auth import login_user, logout_user
from App.controllers.user import validate_User

login_manager = LoginManager()

login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


from App.database import create_db, get_migrate

from App.controllers import (
    setup_jwt,
    create_user
)

from App.models import (
    login,
    user,
    SignUp,
    students,
    conductReviews
)

from App.views import (
    user_views,
    index_views,
    signup_views,
    conduct_views
)

# New views must be imported and added to this list

views = [
    user_views,
    index_views,
    signup_views,
    conduct_views
]

def add_views(app, views):
    for view in views:
        app.register_blueprint(view)

def loadConfig(app, config):
    app.config['ENV'] = os.environ.get('ENV', 'DEVELOPMENT')
    delta = 7
    if app.config['ENV'] == "DEVELOPMENT":
        app.config.from_object('App.config')
        delta = app.config['JWT_EXPIRATION_DELTA']
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'SQLALCHEMY_DATABASE_URI'
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['DEBUG'] = os.environ.get('ENV').upper() != 'PRODUCTION'
        app.config['ENV'] = os.environ.get('ENV')
        delta = os.environ.get('JWT_EXPIRATION_DELTA', 7)
        
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=int(delta))
        
    for key, value in config.items():
        app.config[key] = config[key]

def create_app(config={}):
    app = Flask(__name__, static_url_path='/static')
    CORS(app)
    loadConfig(app, config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app, views)
    create_db(app)
    setup_jwt(app)
    app.app_context().push()
    return app

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/api/users', methods = ['GET'])
def getAllUsers():
    u = User.query.all()
    if u is None:
        return []
    uList = [us.toDict() for us in u]
    return jsonify(uList)


@app.route('/login')
def getLoginPage():
    if current_user.is_authenticated:
        flash('Already Logged In')
        return redirect(url_for('conduct'))
    form = LogIn()
    return render_template('login.html',form = form)

@app.route('/login', methods = {'POST'})
def loginAction():
    form = LogIn()
    data = request.form
    user = validate_User(data['username'], data['password'])
    if user is not None:  
        flash('Login successful')
        login_user(user,True)
        return redirect(url_for('conduct'))
    
    flash('Invalid credentials')
    return redirect(url_for('loginAction'))

@app.route('/signup')
def getSignUpPage():
    if current_user.is_authenticated:
        flash('You cannot create an account while logged in.')
        return redirect(url_for('conduct'))
    form = SignUp()
    return render_template('signup.html',form = form)

@app.route('/signup', methods=['POST'])
def signUpAction():
    form = SignUp()
    data = request.form
    message = create_user(data['username'], data['password'])
    if message == "Error":
        flash('Error. Account not created')
        return redirect(url_for('getSignUpPage'))
    else:
        flash('Account Created Successfully')
    return redirect(url_for('loginAction'))


@app.route('/logout')
def logoutActions():
    logout_user()
    flash('Logged Out')
    return redirect(url_for('index')) 



migrate = get_migrate(app)

