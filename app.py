import os

from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_apispec.extension import FlaskApiSpec
from schemas import PersonSchema, PersonPatchSchema
from flask_apispec import use_kwargs, marshal_with
from flask_migrate import Migrate
import logging
from config import Config

app = Flask(__name__)
app.debug = True
app.config.from_object(Config)
if os.environ.get('GITHUB_WORKFLOW'):
    app.config.update(SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/flask_db'))
db = SQLAlchemy(app)
migrate = Migrate(app, db)

docs = FlaskApiSpec()
docs.init_app(app)

from models import Person
db.create_all()

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler('log/api.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

logger = setup_logger()


@app.route('/')
@app.route('/home')
def hello_world():
    return render_template('main.html')


@app.route('/about')
def about():
    return 'About me!'


@app.route('/create', methods=['POST', 'GET'])
def create():
    persons = Person.query.order_by('firstname').all()
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
            return redirect('/create')
        except:
             return "Error of creating person"
    return render_template('create_index.html', persons=persons)


@app.route('/persons', methods=['GET'])
@marshal_with(PersonSchema(many=True))
def persons_get():
    allpersons = Person.query.order_by(Person.id).all()
    if allpersons is not None:
        return allpersons, 200
    else:
        logger.warning(f'Persons get action failed with error {404}')
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
        response.headers['Location'] = '/persons/' + str(new_person.id)
        response.autocorrect_location_header = True
        return response, 201
    except Exception as e:
        logger.warning(f'Person post action failed with error {e}')
        return {'message': 'ValidationError'}, 422


@app.route('/persons/<int:id>', methods=['GET'])
@marshal_with(PersonSchema)
def persons_detail_get(id):
    person = Person.query.get(id)
    if person is not None:
        return person, 200
    else:
        logger.warning(f'Person {id} get action failed with error {404}')
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
        except Exception as e:
            logger.warning(f'Person {id} patch action failed with error {e}')
            return {'message': 'ValidationError'}, 422
    else:
        logger.warning(f'Person {id} patch action failed with error {404}')
        return {'message': 'Person does not exist'}, 404


@app.route('/persons/<int:id>', methods=['DELETE'])
def persons_detail_delete(id):
    try:
        person = Person.query.get(id)
        db.session.delete(person)
        db.session.commit()
        return '', 204
    except Exception as e:
        logger.warning(f'Person {id} delete action failed with error {e}')
        return jsonify({'message': 'Person does not exist'}), 404


import errors

docs.register(persons_get)
docs.register(persons_post)
docs.register(persons_detail_get)
docs.register(persons_detail_patch)
docs.register(persons_detail_delete)


if __name__ == '__main__':
    app.run(debug=True)
