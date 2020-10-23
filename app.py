from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)

ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kwibemerci:sumbe1224@localhost/flask_db_trial'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Declaring a join table (Avoid using models)
user_address = db.Table('user_addresses',
                        db.Column('user_id', db.ForeignKey('users.id')),
                        db.Column('address_id', db.ForeignKey('addresses.id')),
                        )


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.CHAR(200), nullable=True)
    # One to many relationship definition
    supplies = db.relationship('Supply', backref='user', lazy=True)
    # Many to many relationship definition
    addresses = db.relationship('Address', secondary=user_address,
                                backref=db.backref('user'))
    createdAt = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, name):
        self.name = name


class Supply(db.Model):
    __tablename__ = 'supplies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.CHAR(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    createdAt = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id


class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(500), nullable=False)

    # Many to many relationship definition
    users = db.relationship('User', secondary=user_address,
                            backref=db.backref('address'))
    createdAt = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, address):
        self.address = address


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

'''
Some Queries Created
    ( One to Many Relationships)
- user = db.session.query(User).filter(User.id==1).first()
- supplies_by_ user = user.supplies

- supply = db.session.query(Supply).filter(Supply.id==1).first()
- supply.user

- In the python console run db.create_all to run the migrations
- 
'''
