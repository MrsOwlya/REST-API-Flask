from marshmallow import Schema, validate, fields

class PersonSchema(Schema):
    id = fields.Integer(dump_only=True)
    firstname = fields.String(required=True, validate=[validate.Length(max=20)])
    surname = fields.String(required=True, validate=[validate.Length(max=20)])
    birth = fields.Date(required=True)
    job = fields.String(required=True, validate=[validate.Length(max=20)])
    address = fields.String(required=True, validate=[validate.Length(max=20)])
    message = fields.String(dump_only=True)


class PersonPatchSchema(Schema):
    id = fields.Integer(dump_only=True)
    firstname = fields.String(required=False, validate=[validate.Length(max=20)])
    surname = fields.String(required=False, validate=[validate.Length(max=20)])
    birth = fields.Date(required=False)
    job = fields.String(required=False, validate=[validate.Length(max=20)])
    address = fields.String(required=False, validate=[validate.Length(max=20)])
    message = fields.String(dump_only=False)