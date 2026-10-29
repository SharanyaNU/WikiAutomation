"""AI Engineer Course: Microsoft Agent Framework.

A small Flask site for the course: the catalogue, module pages, and a JSON API
for modules and enrolment.

Run locally:
    python -m venv .venv
    .venv\\Scripts\\pip install -r requirements.txt
    flask --app app run --debug
"""

from flask import Flask, render_template

import db
from api.routes import api_bp
from course.catalog import COURSE, MODULES
from course.routes import course_bp


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(DATABASE="instance/course.sqlite3")
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    app.register_blueprint(course_bp)
    app.register_blueprint(api_bp)

    @app.route("/")
    def index():
        ready = sum(1 for m in MODULES if m.ready)
        return render_template("index.html", course=COURSE, modules=MODULES, ready=ready)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
