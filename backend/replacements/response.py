from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models.product import ATTRIBUTE_MAX, ATTRIBUTE_MIN, Product


class ProductSchema(SQLAlchemyAutoSchema):
    lifecycle_rank = fields.Integer(required=True)
    attributes = fields.Dict(
        required=True,
        keys=fields.String(),
        values=fields.Integer(validate=validate.Range(ATTRIBUTE_MIN, ATTRIBUTE_MAX)),
    )

    class Meta:
        model = Product
        exclude = ("id",)
        include_relationships = False
