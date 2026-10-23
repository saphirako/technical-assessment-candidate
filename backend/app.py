from flask import Flask
from flask_cors import CORS

from health import bp as health_bp
from replacements import bp as replacements_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# TODO: Initialize your database connection here (SQLite, PostgreSQL, or MongoDB)

app.register_blueprint(health_bp)
app.register_blueprint(replacements_bp)


if __name__ == '__main__':
    import os
    # Fix for macOS multiprocessing issues with Flask reloader
    os.environ['FLASK_ENV'] = 'development'
    app.run(host=os.environ.get('FLASK_RUN_HOST'), port=8000, debug=True, use_reloader=False)
