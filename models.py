from app import db

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    birth = db.Column(db.Date, nullable=False)
    job = db.Column(db.String(20), default="Notwork", nullable=False)
    address = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.id