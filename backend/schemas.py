# schemas.py (actualizado)
from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))

class ProductSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    stock = fields.Int(required=True)
    supplier_id = fields.Int(required=True)