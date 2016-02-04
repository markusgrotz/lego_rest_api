#!/usr/bin/env python
from __future__ import print_function, division

import logging

from flask import Flask, render_template
from flask.ext.login import LoginManager, current_user
from flask.ext.restless import APIManager, ProcessingException

from flask_bootstrap import Bootstrap

from db_model import db
from db_model import User, Race, Checkpoint, CheckpointTime

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager()

login_manager.init_app(app)
db.init_app(app)
Bootstrap(app)


@app.route('/times')
@app.route('/times/<int:page>')
def list_times(page=1):
    times = CheckpointTime.query.paginate(page, 400)
    return render_template('checkpoint_times.html', times=times)


@app.route('/user/<username>')
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('show_user.html', user=user)


def auth_func(*args, **kwargs):
    """
    if not is_authorized_to_modify(current_user, instance_id):
    """
    if not current_user.is_authenticated():
        raise ProcessingException(description='Not Authorized', code=401)
    return True


def main():
    logging.basicConfig(level=logging.DEBUG)

    with app.app_context():
        api_manager = APIManager(app, flask_sqlalchemy_db=db, preprocessors=dict(POST=[auth_func]))
        api_manager.create_api(Race, methods=['GET'])
        api_manager.create_api(Checkpoint, methods=['GET'])
        api_manager.create_api(User, methods=['GET'], include_columns=['username'])
        api_manager.create_api(CheckpointTime, methods=['GET', 'POST'])

    app.run()

if __name__ == '__main__':
    main()
