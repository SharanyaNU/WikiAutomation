"""JSON API: modules and enrolment. Progress tracking is not built yet (see README roadmap)."""

import re
import sqlite3

from flask import Blueprint, jsonify, request

import db
from course.catalog import MODULES, find

api_bp = Blueprint("api", __name__, url_prefix="/api")

EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _module_json(m):
    return {"number": m.number, "slug": m.slug, "title": m.title, "summary": m.summary, "ready": m.ready,
            "lessons": [lesson.title for lesson in m.lessons]}


@api_bp.get("/health")
def health():
    return jsonify(status="ok")


@api_bp.get("/modules")
def list_modules():
    return jsonify([_module_json(m) for m in MODULES])


@api_bp.get("/modules/<slug>")
def get_module(slug):
    found = find(slug)
    if found is None:
        return jsonify(error="module not found"), 404
    return jsonify(_module_json(found))


@api_bp.route("/enrollments", methods=["POST"])
def enroll():
    payload = request.get_json(silent=True) or {}
    name = str(payload.get("name", "")).strip()
    email = str(payload.get("email", "")).strip().lower()
    if not name or not EMAIL.match(email):
        return jsonify(error="name and a valid email are required"), 400
    try:
        learner_id = db.add_learner(name, email)
    except sqlite3.IntegrityError:
        return jsonify(error="this email is already enrolled"), 409
    return jsonify(id=learner_id, name=name, email=email, status="enrolled"), 201


@api_bp.get("/enrollments/<int:learner_id>")
def get_enrollment(learner_id):
    learner = db.get_learner(learner_id)
    if learner is None:
        return jsonify(error="learner not found"), 404
    return jsonify(learner)
