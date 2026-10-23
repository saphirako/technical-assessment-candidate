from models.product import (
    ATTRIBUTE_MAX,
    ATTRIBUTE_MIN,
    LIFECYCLE_RANK,
    MPN_PATTERN,
    OPERATING_TEMP_CEILING,
    OPERATING_TEMP_FLOOR,
    SOURCES,
    Product,
)

from .ordering import ORDER_BY_FIELD

FILTER_FIELDS = (
    "source",
    "mpn",
    "classification",
    "lifecycle_status",
    "rohs_compliance",
    "min_operating_temp",
    "max_operating_temp",
    "attributes",
)


def _require_enum(field, value, allowed):
    if value not in allowed:
        raise ValueError(f"{field} must be one of {sorted(allowed)}, got {value!r}")


def _require_int_in_range(field, value, floor, ceiling):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field} must be an integer, got {value!r}")
    if not floor <= value <= ceiling:
        raise ValueError(f"{field} must be between {floor} and {ceiling}, got {value!r}")


def _parse_attributes(value):
    if not isinstance(value, dict):
        raise ValueError(f"attributes must be an object, got {value!r}")
    for key, attribute in value.items():
        if not isinstance(key, str):
            raise ValueError(f"attribute keys must be strings, got {key!r}")
        _require_int_in_range(f"attributes.{key}", attribute, ATTRIBUTE_MIN, ATTRIBUTE_MAX)
    return value


def parse_filters(body):
    if body is None:
        return {}
    if not isinstance(body, dict):
        raise ValueError("request body must be a JSON object")

    unknown = sorted(set(body) - set(FILTER_FIELDS) - {ORDER_BY_FIELD})
    if unknown:
        raise ValueError(f"unknown filter fields: {', '.join(unknown)}")

    filters = {}
    if "source" in body:
        _require_enum("source", body["source"], SOURCES)
        filters["source"] = body["source"]
    if "mpn" in body:
        if not isinstance(body["mpn"], str) or not MPN_PATTERN.fullmatch(body["mpn"]):
            raise ValueError(f"mpn must be a 10-character alphanumeric string, got {body['mpn']!r}")
        filters["mpn"] = body["mpn"]
    if "classification" in body:
        if body["classification"] is not None and not isinstance(body["classification"], str):
            raise ValueError(f"classification must be a string or null, got {body['classification']!r}")
        filters["classification"] = body["classification"]
    if "lifecycle_status" in body:
        _require_enum("lifecycle_status", body["lifecycle_status"], LIFECYCLE_RANK)
        filters["lifecycle_status"] = body["lifecycle_status"]
    if "rohs_compliance" in body:
        if not isinstance(body["rohs_compliance"], bool):
            raise ValueError(f"rohs_compliance must be a boolean, got {body['rohs_compliance']!r}")
        filters["rohs_compliance"] = body["rohs_compliance"]
    if "min_operating_temp" in body:
        _require_int_in_range(
            "min_operating_temp", body["min_operating_temp"], OPERATING_TEMP_FLOOR, OPERATING_TEMP_CEILING
        )
        filters["min_operating_temp"] = body["min_operating_temp"]
    if "max_operating_temp" in body:
        _require_int_in_range(
            "max_operating_temp", body["max_operating_temp"], OPERATING_TEMP_FLOOR, OPERATING_TEMP_CEILING
        )
        filters["max_operating_temp"] = body["max_operating_temp"]
    if (
        "min_operating_temp" in filters
        and "max_operating_temp" in filters
        and filters["min_operating_temp"] > filters["max_operating_temp"]
    ):
        raise ValueError("min_operating_temp must not exceed max_operating_temp")
    if "attributes" in body:
        filters["attributes"] = _parse_attributes(body["attributes"])
    return filters


def apply_filters(query, filters):
    if "source" in filters:
        query = query.where(Product.source == filters["source"])
    if "mpn" in filters:
        query = query.where(Product.mpn == filters["mpn"])
    if "classification" in filters:
        query = query.where(Product.classification == filters["classification"])
    if "lifecycle_status" in filters:
        query = query.where(Product.lifecycle_status == filters["lifecycle_status"])
    if "rohs_compliance" in filters:
        query = query.where(Product.rohs_compliance == filters["rohs_compliance"])
    if "min_operating_temp" in filters:
        query = query.where(Product.min_operating_temp <= filters["min_operating_temp"])
    if "max_operating_temp" in filters:
        query = query.where(Product.max_operating_temp >= filters["max_operating_temp"])
    for key, value in filters.get("attributes", {}).items():
        query = query.where(Product.attributes[key].as_integer() == value)
    return query
