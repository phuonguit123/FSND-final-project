from flask_sqlalchemy import *

db = SQLAlchemy()


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=False)
    actors = db.relationship('Actor', backref='Movie')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }

    def __repr__(self):
        return f'<id: {self.id}, title: {self.title}, release_date: {self.release_date}>'


class Actor(db.Model):
    __tablename__ = 'Actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_id': self.movie_id
        }


    def __repr__(self):
        return f'<id: {self.id}, name: {self.name}, age: {self.age}, gender: {self.gender}>'
