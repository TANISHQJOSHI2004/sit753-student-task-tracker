import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///tasks.db"
)  
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    due_date = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    completed = db.Column(db.Boolean, default=False)


@app.route("/")
def index():
    tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    subject = request.form["subject"]
    title = request.form["title"]
    due_date = request.form["due_date"]
    priority = request.form["priority"]

    task = Task(
        subject=subject,
        title=title,
        due_date=due_date,
        priority=priority
    )

    db.session.add(task)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    task = db.get_or_404(Task, task_id)

    task.completed = not task.completed
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "student-task-tracker"
    }), 200


@app.route("/api/tasks")
def api_tasks():
    tasks = Task.query.all()

    return jsonify([
        {
            "id": task.id,
            "subject": task.subject,
            "title": task.title,
            "due_date": task.due_date,
            "priority": task.priority,
            "completed": task.completed
        }
        for task in tasks
    ])


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)