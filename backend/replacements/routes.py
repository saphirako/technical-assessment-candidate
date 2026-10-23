from flask import Blueprint, jsonify, request

from .filters import parse_filters
from .ordering import parse_order_by
from .search import search_products

bp = Blueprint('replacements', __name__)


@bp.route('/api/replacements', methods=['POST'])
def find_replacements():
    try:
        body = request.get_json(silent=True)
        filters = parse_filters(body)
        order = parse_order_by(body)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(search_products(filters, order))
