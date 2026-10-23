from marshmallow import Schema, ValidationError, fields, validate, validates_schema

from models.product import (
    ATTRIBUTE_MAX,
    ATTRIBUTE_MIN,
    LIFECYCLE_RANK,
    MPN_PATTERN,
    OPERATING_TEMP_CEILING,
    OPERATING_TEMP_FLOOR,
    SOURCES,
)

from .ordering import SORTABLE_FIELDS

ORDER_ENTRY_PATTERN = r"^-?({})$".format("|".join(SORTABLE_FIELDS))


class ReplacementRequest(Schema):
    source = fields.String(load_only=True, validate=validate.OneOf(SOURCES))
    mpn = fields.String(load_only=True, validate=validate.Regexp(MPN_PATTERN.pattern))
    classification = fields.String(load_only=True, allow_none=True)
    lifecycle_status = fields.String(load_only=True, validate=validate.OneOf(LIFECYCLE_RANK))
    rohs_compliance = fields.Boolean(load_only=True)
    min_operating_temp = fields.Integer(
        load_only=True,
        validate=validate.Range(OPERATING_TEMP_FLOOR, OPERATING_TEMP_CEILING),
    )
    max_operating_temp = fields.Integer(
        load_only=True,
        validate=validate.Range(OPERATING_TEMP_FLOOR, OPERATING_TEMP_CEILING),
    )
    attributes = fields.Dict(
        load_only=True,
        keys=fields.String(),
        values=fields.Integer(validate=validate.Range(ATTRIBUTE_MIN, ATTRIBUTE_MAX)),
    )
    order_by = fields.List(
        load_only=True,
        allow_none=True,
        cls_or_instance=fields.String(validate=validate.Regexp(ORDER_ENTRY_PATTERN)),
    )

    @validates_schema
    def validate_operating_band(self, data, **kwargs):
        low = data.get("min_operating_temp")
        high = data.get("max_operating_temp")
        if low is not None and high is not None and low > high:
            raise ValidationError("min_operating_temp must not exceed max_operating_temp")

    @validates_schema
    def validate_order_by_unique(self, data, **kwargs):
        entries = data.get("order_by") or []
        names = [entry[1:] if entry.startswith("-") else entry for entry in entries]
        duplicates = sorted({name for name in names if names.count(name) > 1})
        if duplicates:
            raise ValidationError(f"order_by must not repeat a field: {', '.join(duplicates)}")
