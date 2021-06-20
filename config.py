import os
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin


class Config:
    if os.environ.get('GITHUB_JOB') == 'my_deploy':
        database_path = "postgres://lhusbwbrroozdo:e304101adc4967768d13ea81ac4f5cd4c2a75806f6249dbb4af6b1014991d391@ec2-50-17-255-120.compute-1.amazonaws.com:5432/d2tcus1l0luhaf"
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
