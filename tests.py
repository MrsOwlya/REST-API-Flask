import pytest
from app import app, db, Person


@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def init_database(test_client):

    db.drop_all()
    db.create_all()
    person1 = Person(
        firstname='TestFirstName',
        surname='TestSurname',
        birth="Fri, 17 Apr 1998 00:00:00 GMT",
        job='TestJob',
        address='TestAddress'
    )
    person2 = Person(
        firstname='TestFirstName2',
        surname='TestSurname2',
        birth="Fri, 17 Apr 1998 00:00:00 GMT",
        job='TestJob2',
        address='TestAddress2'
    )
    db.session.add(person1)
    db.session.add(person2)
    db.session.commit()

    yield

    db.session.remove()
    db.drop_all()


def test_get_all_persons(test_client, init_database):
    res = test_client.get('/persons')
    assert res.status_code == 200
    assert len(res.get_json()) == len(Person.query.all())

def test_get_person_by_id(test_client, init_database):
    res = test_client.get('/persons/1')
    assert res.status_code == 200
    assert Person.query.get(1).firstname == 'TestFirstName'

def test_get_person_not_exist(test_client, init_database):
    res = test_client.get('/persons/3000')
    assert res.status_code == 404

def test_post_new_person(test_client, init_database):
    data = {
        "firstname": "UnitName",
        "surname": "UnitSur",
        "birth": "1998-04-17",
        "job": "UnitJob",
        "address": "UnitAddress"
    }
    res = test_client.post('/persons', json=data)
    assert res.status_code == 201
    assert Person.query.get(3).firstname == data['firstname']

def test_post_new_invalid_person(test_client, init_database):
    data = {
        "firstname": "UnitName",
        "birth": "1998-04-17",
        "job": "UnitJob",
        "address": "UnitAddress"
    }
    res = test_client.post('/persons', json=data)
    assert res.status_code == 422

def test_patch_person(test_client, init_database):
    data = {
        "firstname": "UnitName2",
        "job": "UnitJob2"
    }
    res = test_client.patch('/persons/1', json=data)
    assert res.status_code == 200
    assert Person.query.get(1).firstname == 'UnitName2'
    assert Person.query.get(1).job == 'UnitJob2'

def test_delete_person(test_client, init_database):
    res = test_client.delete('/persons/2')
    assert res.status_code == 204
    assert Person.query.get(2) is None