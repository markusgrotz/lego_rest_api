#!/usr/bin/env python
from __future__ import print_function, division

import logging

from flask import render_template
from app_factory import create_app
from db_model import User, CheckpointTime


logger = logging.getLogger(__name__)

app = create_app()


@app.route('/times')
@app.route('/times/<int:page>')
def list_times(page=1):
    times = CheckpointTime.query.paginate(page, 400)
    return render_template('checkpoint_times.html', times=times)


@app.route('/user/<username>')
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('show_user.html', user=user)


def main():
    logging.basicConfig(level=logging.DEBUG)
    logger.info('starting web application')
    app.run()

if __name__ == '__main__':
    main()
