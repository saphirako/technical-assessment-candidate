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


def to_order(order_by):
    if not order_by:
        return [(field, False) for field in DEFAULT_ORDER_BY]
    order = []
    for entry in order_by:
        descending = entry.startswith("-")
        order.append((entry[1:] if descending else entry, descending))
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
