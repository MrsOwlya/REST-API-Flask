import json
import unittest
from flask_migrate import Migrate
from app import app, db, Person


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://owlya:sveya@127.0.0.1:5432/test_db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()
        Migrate(app, db)

        db.create_all()

        self.person1 = Person(
            firstname='TestFirstName',
            surname='TestSurname',
            birth="Fri, 17 Apr 1998 00:00:00 GMT",
            job='TestJob',
            address='TestAddress'
        )
        self.person2 = Person(
            firstname='TestFirstName2',
            surname='TestSurname2',
            birth="Fri, 17 Apr 1998 00:00:00 GMT",
            job='TestJob2',
            address='TestAddress2'
        )
        db.session.add(self.person1)
        db.session.add(self.person2)
        db.session.commit()

    def test_get_all_persons(self):
        res = self.app.get('/persons')
        assert res.status_code == 200
        assert len(res.get_json()) == len(Person.query.all())

    def test_get_person_by_id(self):
        res = self.app.get('/persons/1')
        assert res.status_code == 200
        assert Person.query.get(1).firstname == 'TestFirstName'

    def test_get_person_not_exist(self):
        res = self.app.get('/persons/3000')
        assert res.status_code == 404

    def test_post_new_person(self):
        data = {
            "firstname": "UnitName",
            "surname": "UnitSur",
            "birth": "1998-04-17",
            "job": "UnitJob",
            "address": "UnitAddress"
        }
        res = self.app.post('/persons', json=data)
        assert res.status_code == 201
        assert Person.query.get(3).firstname == data['firstname']

    def test_post_new_invalid_person(self):
        data = {
            "firstname": "UnitName",
            "birth": "1998-04-17",
            "job": "UnitJob",
            "address": "UnitAddress"
        }
        res = self.app.post('/persons', json=data)
        assert res.status_code == 422

    def test_patch_person(self):
        data = {
            "firstname": "UnitName2",
            "job": "UnitJob2"
        }
        res = self.app.patch('/persons/1', json=data)
        assert res.status_code == 200
        assert Person.query.get(1).firstname == 'UnitName2'
        assert Person.query.get(1).job == 'UnitJob2'

    def test_delete_person(self):
        res = self.app.delete('/persons/2')
        assert res.status_code == 204
        assert Person.query.get(2) is None

    def tearDown(self):
        db.session.remove()
        db.drop_all()