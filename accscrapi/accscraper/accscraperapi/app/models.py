from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from . import db


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Unicode(255, collation='utf8_general_ci'))
    last_name = db.Column(db.Unicode(255, collation='utf8_general_ci'))

    filters = relationship('Filter', backref="node", uselist=False)

    def __init__(self, id, first_name, last_name, price, size, distance):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.filters = Filter(id, price, size, distance)

    def __repr__(self):
        return '<UserId: %s> %s %s' % (self.id, self.first_name, self.last_name)

class Filter(db.Model):
    __tablename__ = 'filter'

    fid = db.Column(db.Integer, ForeignKey(User.id), primary_key=True)
    price = db.Column(db.Integer)
    size = db.Column(db.Integer)
    distance = db.Column(db.Integer)

    def __init__(self, id, price, size, distance):
        self.fid = id
        self.price = price
        self.size = size
        self.distance = distance

    def __repr__(self):
        return '<Filter: %s> price: %s  size: %s  distance: %s' % (self.fid, self.price, self.size, self.distance)