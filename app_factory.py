from flask import Flask

from flask_bootstrap import Bootstrap
from flask.ext.login import LoginManager, current_user
from flask.ext.restless import APIManager, ProcessingException

from db_model import db
from db_model import User, Race, Checkpoint, CheckpointTime


def auth_func(*args, **kwargs):
    """
    if not is_authorized_to_modify(current_user, instance_id):
    """
    if not current_user.is_authenticated():
        raise ProcessingException(description='Not Authorized', code=401)
    return True


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    login_manager = LoginManager()

    api_manager = APIManager()
    api_manager.create_api(Race, methods=['GET'])
    api_manager.create_api(Checkpoint, methods=['GET'])
    api_manager.create_api(User, methods=['GET'], include_columns=['username'])
    api_manager.create_api(CheckpointTime, collection_name='time',
                           methods=['GET', 'POST', 'PUT'],
                           preprocessors=dict(POST=[auth_func]))

    with app.app_context():
        login_manager.init_app(app)
        db.init_app(app)
        api_manager.init_app(app, flask_sqlalchemy_db=db)
        Bootstrap(app)

    return app
