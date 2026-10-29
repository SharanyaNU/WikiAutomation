from flask import Blueprint, abort, render_template

from .catalog import COURSE, MODULES, find

course_bp = Blueprint("course", __name__, url_prefix="/course")


@course_bp.route("/")
def catalogue():
    return render_template("catalogue.html", course=COURSE, modules=MODULES)


@course_bp.route("/<slug>")
def module(slug):
    found = find(slug)
    if found is None:
        abort(404)
    if not found.ready:
        return render_template("coming_soon.html", course=COURSE, module=found), 200
    return render_template("module.html", course=COURSE, module=found)
