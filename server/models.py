from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'
                        # many activities have many campers
    serialize_rules = ('-activities.campers', '-signups')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Here we told it to point to the Signup class and load multiple of those.
    # backref is a simple way to also declare a new property on the Signup class. 
    # You can then also use signup.camper to get to the camper at that signup
    signups = db.relationship('Signup', backref='camper')
                                    # =("table", "table's column")
    activities = association_proxy('signups', 'activity')

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Must have a name')
        return name
    @validates('age')
    def validate_age(self, key, age):
        if not 8 <= age <= 18:
            raise ValueError('Age must be between 8 and 18')
        return age

    def __repr__(self):
        return f'<Camper {self.name} {self.age} />'

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'
                        # many campers have many activities
    serialize_rules = ('-campers.activities', '-signups')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    signups = db.relationship('Signup', backref='activity')
    campers = association_proxy('signups', 'camper')

    def __repr__(self):
        return f'<Activity {self.name} {self.difficulty} />'

class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'
    
    # one to many so singular to plural
    serialize_rules = ('-camper.activities', '-activity.campers')

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    @validates('time')
    def validate_age(self, key, time):
        if not 0 <= time <= 23:
            raise ValueError('Must be between 0 and 23 (hour)')
        return time

    def __repr__(self):
        return f'<Signup {self.time}/>'

