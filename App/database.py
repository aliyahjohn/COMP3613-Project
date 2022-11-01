from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def get_migrate(app):
    return Migrate(app, db)

def create_db(app):
    db.init_app(app)
    
    # db.create_all(app=app)
    # CAUSING ERROR: 
    # AttributeError: 'NoneType' object has no attribute 'drivername'
    
def init_db(app):
    db.init_app(app)