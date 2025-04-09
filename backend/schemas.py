from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    class Meta:
        ordered = True
    name = fields.Str(required=True, validate=validate.Length(min=2))
    barcode = fields.Str(required=True)
    stock = fields.Int(validate=validate.Range(min=0))
    price = fields.Float(required=True)

class SaleSchema(Schema):
    items = fields.List(
        fields.Dict(keys=fields.Str(), values=fields.Raw()),
        required=True
    )