from uuid import UUID

from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import http_status_message
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://owlya:sveya@127.0.0.1:5432/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    birth = db.Column(db.Date, nullable=False)
    job = db.Column(db.String(20), default="Notwork", nullable=False)
    address = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.id

db.create_all()


@app.route('/')
@app.route('/home')
def hello_world():
    return render_template('index.html')


@app.route('/about')
def about():
    return 'About me!'


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        firstname = request.form['firstname']
        surname = request.form['surname']
        birth = request.form['birth']
        job = request.form['job']
        address = request.form['address']

        person = Person(
            firstname=firstname,
            surname=surname,
            birth=birth,
            job=job,
            address=address
        )

        try:
            db.session.add(person)
            db.session.commit()
            return redirect('/')
        except:
             return "Error of creating person"
    else:
        return render_template('create.html')


@app.route('/persons', methods=['POST', 'GET'])
def persons():
    if request.method == 'GET':
        try:
            persons = Person.query.order_by(Person.firstname).all()
            serialized = []
            for person in persons:
                serialized.append({
                    'id': person.id,
                    'firstname': person.firstname,
                    'surname': person.surname,
                    'birth': person.birth,
                    'job': person.job,
                    'address': person.address
                })
            return jsonify(serialized), 200
        except:
            return jsonify({'message': 'No objects'}), 404

    if request.method == 'POST':
        new_person = Person(**request.json)
        db.session.add(new_person)
        db.session.commit()
        serialized = {
            'id': new_person.id,
            'firstname': new_person.firstname,
            'surname': new_person.surname,
            'birth': new_person.birth,
            'job': new_person.job,
            'address': new_person.address
        }
        return jsonify(serialized), 201


@app.route('/persons/<int:id>', methods=['POST', 'GET', 'PATCH', 'DELETE'])
def persons_detail(id):
    try:
        person = Person.query.get(id)
    except:
        return jsonify({'message': 'Person does not exist'}), 404

    if request.method == 'GET':
        try:
            serialized = {
                'id': person.id,
                'firstname': person.firstname,
                'surname': person.surname,
                'birth': person.birth,
                'job': person.job,
                'address': person.address
            }
            return jsonify(serialized), 200
        except:
            return jsonify({'message': 'Error of serialization'}), 404

    if request.method == 'PATCH':
        params = request.json
        for key, value in params.items():
            setattr(person, key, value)
        db.session.commit()
        serialized = {
            'id': person.id,
            'firstname': person.firstname,
            'surname': person.surname,
            'birth': person.birth,
            'job': person.job,
            'address': person.address
        }
        return jsonify(serialized), 200

    if request.method == 'DELETE':
        db.session.delete(person)
        db.session.commit()
        return jsonify({'message': 'Person deleted'}), 204


if __name__ == '__main__':
    app.run(debug=True)
