#!/usr/bin/env python

import logging
import argparse

from main import app

from db_model import db
from db_model import User, Race, Checkpoint, CheckpointTime

logger = logging.getLogger(__name__)


def add_test_data():
    u = User('foo')
    db.session.add(u)

    u2 = User('bar')
    db.session.add(u2)

    c1 = Checkpoint('start')
    c2 = Checkpoint('finish')
    db.session.add(c1)
    db.session.add(c2)
    db.session.commit()

    r = Race([u])
    db.session.add(r)
    db.session.commit()

    t = CheckpointTime(r, c1, u, 0)
    db.session.add(t)
    t = CheckpointTime(r, c2, u, 0)
    db.session.add(t)

    t = CheckpointTime(r, c1, u, 1)
    db.session.add(t)
    t = CheckpointTime(r, c2, u, 1)
    db.session.add(t)

    t = CheckpointTime(r, c1, u2, 0)
    db.session.add(t)
    t = CheckpointTime(r, c2, u2, 0)
    db.session.add(t)
    db.session.commit()


def main():

    parser = argparse.ArgumentParser(description="")

    parser.add_argument('-c', '--create-db', action='store_true', help='create database')
    parser.add_argument('-d', '--drop-db', action='store_true', help='drop database')
    parser.add_argument('-t', '--test-data', action='store_true', help='add test data')

    args = parser.parse_args()

    with app.app_context():
        if args.drop_db:
            db.drop_all()

        if args.create_db:
            db.create_all()

        if args.test_data:
            add_test_data()

if __name__ == '__main__':
    main()
