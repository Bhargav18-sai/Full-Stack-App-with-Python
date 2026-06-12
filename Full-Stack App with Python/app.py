# ============================================================
#  Full-Stack Todo App  —  Backend (Python + Flask + SQLite)
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os

app = Flask(__name__)
DB = "todos.db"

# ── Database helpers ─────────────────────────────────────────

def get_db():
    """Open a fresh DB connection for each request."""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row   # rows behave like dicts
    return conn

def init_db():
    """Create the todos table if it doesn't exist yet."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                task      TEXT    NOT NULL,
                done      INTEGER NOT NULL DEFAULT 0,
                created   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

# ── Routes ───────────────────────────────────────────────────

@app.route("/")
def index():
    """Home page — show all todos."""
    filter_by = request.args.get("filter", "all")

    with get_db() as conn:
        if filter_by == "active":
            rows = conn.execute("SELECT * FROM todos WHERE done=0 ORDER BY id DESC").fetchall()
        elif filter_by == "done":
            rows = conn.execute("SELECT * FROM todos WHERE done=1 ORDER BY id DESC").fetchall()
        else:
            rows = conn.execute("SELECT * FROM todos ORDER BY id DESC").fetchall()

    todos = [dict(row) for row in rows]
    return render_template("index.html", todos=todos, filter=filter_by)


@app.route("/add", methods=["POST"])
def add_todo():
    """Add a new todo item."""
    task = request.form.get("task", "").strip()
    if task:
        with get_db() as conn:
            conn.execute("INSERT INTO todos (task) VALUES (?)", (task,))
            conn.commit()
    return redirect(url_for("index"))


@app.route("/toggle/<int:todo_id>")
def toggle_todo(todo_id):
    """Mark a todo done ↔ undone."""
    with get_db() as conn:
        conn.execute("UPDATE todos SET done = 1 - done WHERE id = ?", (todo_id,))
        conn.commit()
    return redirect(request.referrer or url_for("index"))


@app.route("/delete/<int:todo_id>")
def delete_todo(todo_id):
    """Delete a todo item."""
    with get_db() as conn:
        conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
    return redirect(request.referrer or url_for("index"))


@app.route("/edit/<int:todo_id>", methods=["POST"])
def edit_todo(todo_id):
    """Rename a todo item (called via fetch from JS)."""
    data = request.get_json()
    new_task = data.get("task", "").strip()
    if new_task:
        with get_db() as conn:
            conn.execute("UPDATE todos SET task = ? WHERE id = ?", (new_task, todo_id))
            conn.commit()
        return jsonify({"success": True, "task": new_task})
    return jsonify({"success": False}), 400


# ── API endpoint (bonus) ─────────────────────────────────────

@app.route("/api/todos")
def api_todos():
    """Return all todos as JSON — useful for testing / extensions."""
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM todos ORDER BY id DESC").fetchall()
    return jsonify([dict(row) for row in rows])


# ── Start ────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    print("\n✅  Todo App running at  http://127.0.0.1:5000\n")
    app.run(debug=True)
