from flask import Flask
from flask_cors import CORS

from health import bp as health_bp
from openapi import api
from replacements import bp as replacements_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

app.config.update(
    API_TITLE="Product Replacement Search",
    API_VERSION="1.0.0",
    OPENAPI_VERSION="3.0.3",
    OPENAPI_URL_PREFIX="/",
    OPENAPI_JSON_PATH="swagger",
    OPENAPI_SWAGGER_UI_PATH="/docs",
    OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
)

api.init_app(app)
api.register_blueprint(health_bp)
api.register_blueprint(replacements_bp)


if __name__ == '__main__':
    import os
    # Fix for macOS multiprocessing issues with Flask reloader
    os.environ['FLASK_ENV'] = 'development'
    app.run(host=os.environ.get('FLASK_RUN_HOST'), port=8000, debug=True, use_reloader=False)
