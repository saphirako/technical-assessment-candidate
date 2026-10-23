from sqlalchemy import func, select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.exc import SQLAlchemyError

from db import Base, SessionLocal, engine
from models.product import Product, lifecycle_rank
from starter import product_generator, reset_generator

DEFAULT_LIMIT = 1000


def clean_product(raw: dict) -> Product | None:
    try:
        return Product(
            source=raw.get("source"),
            mpn=raw.get("mpn"),
            classification=raw.get("classification"),
            lifecycle_status=raw.get("lifecycle_status"),
            rohs_compliance=raw.get("rohs_compliance"),
            min_operating_temp=raw.get("min_operating_temp"),
            max_operating_temp=raw.get("max_operating_temp"),
            attributes=raw.get("additional_data"),
        )
    except (SQLAlchemyError, ValueError):
        return None


def upsert_product(session, product: Product) -> int:
    statement = insert(Product).values(
        source=product.source,
        mpn=product.mpn,
        classification=product.classification,
        lifecycle_status=product.lifecycle_status,
        rohs_compliance=product.rohs_compliance,
        min_operating_temp=product.min_operating_temp,
        max_operating_temp=product.max_operating_temp,
        attributes=product.attributes,
    )
    incoming = statement.excluded
    return session.execute(
        statement.on_conflict_do_update(
            index_elements=[Product.mpn, Product.source],
            set_={
                "source": incoming.source,
                "classification": incoming.classification,
                "lifecycle_status": incoming.lifecycle_status,
                "rohs_compliance": incoming.rohs_compliance,
                "min_operating_temp": incoming.min_operating_temp,
                "max_operating_temp": incoming.max_operating_temp,
                "attributes": incoming.attributes,
            },
            where=lifecycle_rank(Product.lifecycle_status)
            > lifecycle_rank(incoming.lifecycle_status),
        )
    ).rowcount


def populate(limit: int = DEFAULT_LIMIT) -> None:
    Base.metadata.create_all(engine)
    reset_generator()

    invalid = 0
    written = 0
    with SessionLocal() as session, session.begin():
        for index, raw in enumerate(product_generator()):
            if index >= limit:
                break
            product = clean_product(raw)
            if product is None:
                invalid += 1
                continue
            written += upsert_product(session, product)

    skipped = limit - invalid - written
    with SessionLocal() as session:
        canonical = session.scalar(select(func.count()).select_from(Product))
    print(
        f"Read {limit} raw products: {invalid} invalid dropped, "
        f"{skipped} skipped for lower-or-equal lifecycle, "
        f"{canonical} canonical products stored"
    )


if __name__ == "__main__":
    populate()
