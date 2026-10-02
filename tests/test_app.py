import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest

from app import app, db, Task


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Student Task Tracker" in response.data


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"
    assert data["service"] == "student-task-tracker"


def test_add_task(client):
    response = client.post(
        "/add",
        data={
            "subject": "SIT753",
            "title": "Complete DevOps Pipeline",
            "due_date": "2026-10-10",
            "priority": "High"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Complete DevOps Pipeline" in response.data
    assert b"SIT753" in response.data


def test_api_tasks(client):
    task = Task(
        subject="SIT753",
        title="Test Jenkins Pipeline",
        due_date="2026-10-15",
        priority="Medium"
    )

    with app.app_context():
        db.session.add(task)
        db.session.commit()

    response = client.get("/api/tasks")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["subject"] == "SIT753"
    assert data[0]["title"] == "Test Jenkins Pipeline"


def test_complete_task(client):
    with app.app_context():
        task = Task(
            subject="SIT753",
            title="Finish Testing",
            due_date="2026-10-20",
            priority="High"
        )

        db.session.add(task)
        db.session.commit()

        task_id = task.id

    response = client.get(
        f"/complete/{task_id}",
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        task = db.session.get(Task, task_id)
        assert task.completed is True


def test_delete_task(client):
    with app.app_context():
        task = Task(
            subject="SIT753",
            title="Temporary Task",
            due_date="2026-10-25",
            priority="Low"
        )

        db.session.add(task)
        db.session.commit()

        task_id = task.id

    response = client.get(
        f"/delete/{task_id}",
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        task = db.session.get(Task, task_id)
        assert task is None