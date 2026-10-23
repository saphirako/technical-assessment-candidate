from models.product import Product


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
