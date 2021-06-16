from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from schemas import PersonSchema, PersonPatchSchema
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

from models import Person
db.create_all()


@app.route('/')
@app.route('/home')
def hello_world():
    return render_template('index.html')


@app.route('/read')
def read():
    return render_template('read.html')


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
        return {'message': 'No persons'}, 404


@app.route('/persons', methods=['POST'])
@use_kwargs(PersonSchema)
@marshal_with(PersonSchema)
def persons_post(**kwargs):
    try:
        new_person = Person(**kwargs)
        db.session.add(new_person)
        db.session.commit()
        response = jsonify()
        response.status_code = 201
        response.headers['Location'] = '/persons/' + str(new_person.id)
        response.autocorrect_location_header = True
        return response
    except:
        return {'message': 'ValidationError'}, 422


@app.route('/persons/<int:id>', methods=['GET'])
@marshal_with(PersonSchema)
def persons_detail_get(id):
    person = Person.query.get(id)
    if person is not None:
        return person, 200
    else:
        return {'message': 'Person does not exist'}, 404


@app.route('/persons/<int:id>', methods=['PATCH'])
@use_kwargs(PersonPatchSchema)
@marshal_with(PersonPatchSchema)
def persons_detail_patch(id, **kwargs):
    person = Person.query.get(id)
    if person is not None:
        try:
            for key, value in kwargs.items():
                setattr(person, key, value)
            db.session.commit()
            return person, 200
        except:
            return {'message': 'ValidationError'}, 422
    else:
        return {'message': 'Person does not exist'}, 404


@app.route('/persons/<int:id>', methods=['DELETE'])
def persons_detail_delete(id):
    try:
        person = Person.query.get(id)
        db.session.delete(person)
        db.session.commit()
        return {'message': 'Person deleted'}, 204
    except:
        return {'message': 'Person does not exist'}, 404


@app.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


docs.register(persons_get)
docs.register(persons_post)
docs.register(persons_detail_get)
docs.register(persons_detail_patch)
docs.register(persons_detail_delete)


if __name__ == '__main__':
    app.run(debug=True)
