from sqlalchemy import select

from db import SessionLocal
from models.product import LIFECYCLE_RANK, Product

from .filters import apply_filters
from .ordering import apply_order


def build_query(filters, order):
    return apply_order(apply_filters(select(Product), filters), order)


def serialize_product(product):
    return {
        "source": product.source,
        "mpn": product.mpn,
        "classification": product.classification,
        "lifecycle_status": product.lifecycle_status,
        "lifecycle_rank": LIFECYCLE_RANK[product.lifecycle_status],
        "rohs_compliance": product.rohs_compliance,
        "min_operating_temp": product.min_operating_temp,
        "max_operating_temp": product.max_operating_temp,
        "attributes": product.attributes,
    }


def search_products(filters, order):
    with SessionLocal() as session:
        products = session.scalars(build_query(filters, order)).all()
    return [serialize_product(product) for product in products]
