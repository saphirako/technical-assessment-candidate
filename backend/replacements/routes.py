from flask.views import MethodView
from flask_smorest import Blueprint

from .ordering import to_order
from .request import ReplacementRequest
from .response import ProductSchema
from .search import search_products

bp = Blueprint("replacements", __name__)


@bp.route("/api/replacements", methods=["POST"])
class ReplacementList(MethodView):
    @bp.doc(
        summary="Search for replacement products",
        description=(
            "Returns products matching any combination of the supplied filters. "
            "Temperature bands use containment: a product matches when its range "
            "covers the requested range. Results default to lifecycle preference "
            "(Active first); use order_by with a '-' prefix for descending."
        ),
    )
    @bp.arguments(ReplacementRequest, location="json", required=False)
    @bp.response(200, ProductSchema(many=True))
    def post(self, payload):
        order = to_order(payload.pop("order_by", None))
        return search_products(payload, order)
