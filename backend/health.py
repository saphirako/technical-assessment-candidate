from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields

bp = Blueprint("health", __name__)


class HealthSchema(Schema):
    status = fields.String(required=True)


@bp.route("/health")
class Health(MethodView):
    @bp.doc(summary="Service health check")
    @bp.response(200, HealthSchema)
    def get(self):
        return {"status": "ok"}
