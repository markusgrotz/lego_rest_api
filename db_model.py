from datetime import datetime

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin

db = SQLAlchemy()


participants = db.Table('race_participants',
                        db.Column('race_id', db.Integer, db.ForeignKey('race.id')),
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')))


class Race(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime(timezone=True))

    participants = db.relationship('User', secondary=participants,
                                   backref=db.backref('haha', lazy='dynamic'))

    def __init__(self, participants):
        self.start_time = datetime.now()
        self.participants = participants

    def __repr__(self):
        return '<Race {}>'.format(self.start_time.isoformat())


class Checkpoint(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    checkpoint_name = db.Column(db.String(80), unique=True)

    def __init__(self, checkpoint_name):
        self.checkpoint_name = checkpoint_name

    def __repr__(self):
        return '<Checkpoint %r>' % self.checkpoint_name


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.username


class Marker(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    x = db.Column(db.Float)
    y = db.Column(db.Float)
    heading = db.Column(db.Float)


class CheckpointTime(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime(timezone=True))

    lap_num = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('times', lazy='dynamic'))

    race_id = db.Column(db.Integer, db.ForeignKey('race.id'))
    race = db.relationship('Race', backref=db.backref('times', lazy='dynamic'))

    checkpoint_id = db.Column(db.Integer, db.ForeignKey('checkpoint.id'))
    checkpoint = db.relationship('Checkpoint', backref=db.backref('times', lazy='dynamic'))

    def __init__(self, race, checkpoint, user, lap_num):
        self.race = race
        self.user = user
        self.checkpoint = checkpoint
        self.lap_num = lap_num
        self.time = datetime.now()

    def __repr__(self):
        return '<Checkpoint {}: {} - {}>'.format(self.checkpoint, self.user, self.time)
