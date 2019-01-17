from flask import Flask
from instance.config import app_config
from app.api.v1.views.meetups_views import v1 as meetups_blueprint
from app.api.v1.views.questions_views import v1 as questions_blueprint
from app.api.v1.views.users_views import v1 as users_blueprint
from app.api.v1.views.comments_views import v1 as comments_blueprint

def create_app(config_name):
    """ Function to initialize Flask app """

    # Initialize app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.register_blueprint(meetups_blueprint)
    
    return app

