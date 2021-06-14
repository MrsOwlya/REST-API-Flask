from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from schemas import PersonSchema
from flask_apispec import use_kwargs, marshal_with

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://owlya:sveya@127.0.0.1:5432/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

docs = FlaskApiSpec()
docs.init_app(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='REST-API-Flask',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()]
    ),
    'APISPEC_SWAGGER_URL': '/swagger/'
})

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


@app.route('/persons', methods=['GET'])
@marshal_with(PersonSchema(many=True))
def persons_get():
    try:
        allpersons = Person.query.order_by(Person.id).all()
        return allpersons, 200
    except:
        return {'message': 'No objects'}, 404


@app.route('/persons', methods=['POST'])
@use_kwargs(PersonSchema)
@marshal_with(PersonSchema)
def persons_post(**kwargs):
    new_person = Person(**kwargs)
    db.session.add(new_person)
    db.session.commit()
    return new_person, 201


@app.route('/persons/<int:id>', methods=['GET'])
@marshal_with(PersonSchema)
def persons_detail_get(id):
    try:
        oneperson = Person.query.get(id)
        return oneperson, 200
    except:
        return {'message': 'Person does not exist'}, 404


@app.route('/persons/<int:id>', methods=['PATCH'])
@use_kwargs(PersonSchema)
@marshal_with(PersonSchema)
def persons_detail_patch(id, **kwargs):
    person = Person.query.get(id)
    for key, value in kwargs.items():
        setattr(person, key, value)
    db.session.commit()
    return person, 200


@app.route('/persons/<int:id>', methods=['DELETE'])
def persons_detail_delete(id):
    person = Person.query.get(id)
    db.session.delete(person)
    db.session.commit()
    return {'message': 'Person deleted'}, 204


if __name__ == '__main__':
    app.run(debug=True)
