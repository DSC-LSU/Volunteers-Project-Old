from flask_sqlalchemy import SQLAlchemy
from utils.phoneutils import *

SQLALCHEMY_DATABASE_URI = 'postgres://{}:{}@{}/{}'.format('postgres',
                                                          'Ropac123',
                                                          'localhost:5432',
                                                          'volunteersapp')

db = SQLAlchemy()


def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String())

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': get_phone_display_format(self.phone)
        }

    def insert(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)
