import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    return create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.sqlite3")}).test_client()


def test_home_shows_progress(client):
    page = client.get("/").get_data(as_text=True)
    assert "AI Engineer Course" in page and "1 of 10 modules published" in page


def test_catalogue_and_modules(client):
    assert "Coming soon" in client.get("/course/").get_data(as_text=True)
    module = client.get("/course/introduction").get_data(as_text=True)
    assert "Your first workflow" in module and "WorkflowBuilder" in module
    assert "being written" in client.get("/course/tools").get_data(as_text=True)
    assert client.get("/course/nope").status_code == 404


def test_modules_api(client):
    modules = client.get("/api/modules").get_json()
    assert len(modules) == 10 and [m["ready"] for m in modules].count(True) == 1
    assert client.get("/api/modules/introduction").get_json()["lessons"][0] == "From a model call to an agent"
    assert client.get("/api/modules/nope").status_code == 404
    assert client.get("/api/health").get_json() == {"status": "ok"}


def test_enrollment(client):
    created = client.post("/api/enrollments", json={"name": "Ada", "email": "Ada@Example.com"})
    assert created.status_code == 201 and created.get_json()["email"] == "ada@example.com"
    learner = client.get(f"/api/enrollments/{created.get_json()['id']}").get_json()
    assert learner["course"] == "ai-engineer"
    assert client.post("/api/enrollments", json={"name": "Ada", "email": "ada@example.com"}).status_code == 409
    assert client.post("/api/enrollments", json={"name": "", "email": "bad"}).status_code == 400
    assert client.get("/api/enrollments/999").status_code == 404


def test_lesson_code_sample_compiles():
    from course.catalog import FIRST_WORKFLOW

    compile(FIRST_WORKFLOW, "first_workflow.py", "exec")
