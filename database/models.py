from flask_sqlalchemy import SQLAlchemy

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
    __tablename__ = 'volunteer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __init__(self, name):
        self.name = name

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def insert(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

