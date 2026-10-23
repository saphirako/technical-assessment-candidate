import re

from sqlalchemy import JSON, Boolean, CheckConstraint, Integer, String, UniqueConstraint, case
from sqlalchemy.orm import Mapped, mapped_column, validates

from db import Base

SOURCES = ("Source A", "Source B", "Source C", "Source D", "Source E")
LIFECYCLE_RANK = {"Active": 0, "End of Life": 1, "Obsolete": 2}
OPERATING_TEMP_FLOOR = -40
OPERATING_TEMP_CEILING = 85
ATTRIBUTE_MIN = 0
ATTRIBUTE_MAX = 4
MPN_PATTERN = re.compile(r"[A-Za-z0-9]{10}")

sources_str_list = ', '.join(repr(s) for s in SOURCES)
lifecycle_str_list = ', '.join(repr(s) for s in LIFECYCLE_RANK)


def lifecycle_rank(status):
    return case(
        *[(status == name, rank) for name, rank in LIFECYCLE_RANK.items()],
        else_=len(LIFECYCLE_RANK),
    )


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (UniqueConstraint("mpn", "source"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(
        String,
        CheckConstraint(f"source IN ({sources_str_list})"),
    )
    mpn: Mapped[str] = mapped_column(
        String(10),
        CheckConstraint("length(mpn) = 10"),
    )
    classification: Mapped[str | None] = mapped_column(String)
    lifecycle_status: Mapped[str] = mapped_column(
        String,
        CheckConstraint(f"lifecycle_status IN ({lifecycle_str_list})"),
    )
    rohs_compliance: Mapped[bool] = mapped_column(Boolean)
    min_operating_temp: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            f"min_operating_temp BETWEEN {OPERATING_TEMP_FLOOR} AND {OPERATING_TEMP_CEILING}"
        ),
    )
    max_operating_temp: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            f"max_operating_temp BETWEEN {OPERATING_TEMP_FLOOR} AND {OPERATING_TEMP_CEILING} "
            "AND max_operating_temp >= min_operating_temp"
        ),
    )
    attributes: Mapped[dict] = mapped_column(JSON, default=dict)

    @validates("source")
    def validate_source(self, key, value):
        if value not in SOURCES:
            raise ValueError(f"invalid source: {value!r}")
        return value

    @validates("mpn")
    def validate_mpn(self, key, value):
        if not isinstance(value, str) or not MPN_PATTERN.fullmatch(value):
            raise ValueError(f"invalid mpn: {value!r}")
        return value

    @validates("lifecycle_status")
    def validate_lifecycle_status(self, key, value):
        if value not in LIFECYCLE_RANK:
            raise ValueError(f"invalid lifecycle_status: {value!r}")
        return value

    @validates("rohs_compliance")
    def validate_rohs_compliance(self, key, value):
        if not isinstance(value, bool):
            raise ValueError(f"rohs_compliance must be a bool: {value!r}")
        return value

    @validates("min_operating_temp", "max_operating_temp")
    def validate_operating_temp(self, key, value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{key} must be an integer: {value!r}")
        if not OPERATING_TEMP_FLOOR <= value <= OPERATING_TEMP_CEILING:
            raise ValueError(
                f"{key} outside {OPERATING_TEMP_FLOOR}..{OPERATING_TEMP_CEILING}: {value!r}"
            )
        min_temp = value if key == "min_operating_temp" else self.min_operating_temp
        max_temp = value if key == "max_operating_temp" else self.max_operating_temp
        if min_temp is not None and max_temp is not None and min_temp > max_temp:
            raise ValueError(f"min_operating_temp {min_temp} exceeds max_operating_temp {max_temp}")
        return value

    @validates("attributes")
    def validate_attributes(self, key, value):
        if not isinstance(value, dict):
            return {}
        return {
            name: attribute
            for name, attribute in value.items()
            if isinstance(attribute, int)
            and not isinstance(attribute, bool)
            and ATTRIBUTE_MIN <= attribute <= ATTRIBUTE_MAX
        }
