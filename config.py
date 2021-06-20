import os
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin


class Config:
    if os.environ.get('GITHUB_WORKFLOW'):
        database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format('postgres', 'postgres', 'localhost:5432', 'flask_db')
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', database_path)
    else:
        SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://owlya:sveya@localhost:5432/test_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '025b376adf584b72888bffe69f90524e'
    APISPEC_SPEC = APISpec(
        title='REST-API-Flask',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()]
    )
    APISPEC_SWAGGER_URL = '/swagger/'
