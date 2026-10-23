from models.product import Product, lifecycle_rank

SORTABLE_FIELDS = (
    "lifecycle_rank",
    "mpn",
    "source",
    "classification",
    "lifecycle_status",
    "rohs_compliance",
    "min_operating_temp",
    "max_operating_temp",
)
DEFAULT_ORDER_BY = ("lifecycle_rank",)
ORDER_BY_FIELD = "order_by"


def parse_order_by(body):
    value = body.get(ORDER_BY_FIELD) if isinstance(body, dict) else None
    if value is None or value == []:
        return [(field, False) for field in DEFAULT_ORDER_BY]
    if not isinstance(value, list) or not all(isinstance(entry, str) for entry in value):
        raise ValueError("order_by must be a list of field names, '-' prefix for descending")
    order = []
    seen = set()
    for entry in value:
        descending = entry.startswith("-")
        field = entry[1:] if descending else entry
        if field not in SORTABLE_FIELDS:
            raise ValueError(f"order_by field must be one of {sorted(SORTABLE_FIELDS)}, got {entry!r}")
        if field in seen:
            raise ValueError(f"order_by must not repeat a field: {field}")
        seen.add(field)
        order.append((field, descending))
    return order


def apply_order(query, order):
    criteria = []
    for field, descending in order:
        expression = (
            lifecycle_rank(Product.lifecycle_status)
            if field == "lifecycle_rank"
            else getattr(Product, field)
        )
        criteria.append(expression.desc() if descending else expression.asc())
    criteria.extend([Product.mpn.asc(), Product.source.asc()])
    return query.order_by(*criteria)
