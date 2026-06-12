# 📝 Full-Stack Todo App (Python + Flask)

A beginner-friendly full-stack web app built with:
- **Backend** → Python + Flask + SQLite
- **Frontend** → HTML + CSS + Vanilla JavaScript

---

## 📁 Project Structure

```
todo-app/
├── app.py               ← Flask backend (all routes & DB logic)
├── todos.db             ← SQLite database (auto-created on first run)
├── requirements.txt     ← Python dependencies
├── templates/
│   └── index.html       ← Jinja2 HTML template
└── static/
    ├── style.css        ← All styling
    └── script.js        ← Inline edit feature (JavaScript)
```

---

## 🚀 How to Run

### 1. Install Python
Make sure Python 3.8+ is installed: https://python.org

### 2. Install Flask
```bash
pip install -r requirements.txt
```

### 3. Start the server
```bash
python app.py
```

### 4. Open in browser
```
http://127.0.0.1:5000
```

---

## ✅ Features

| Feature          | How it works                        |
|------------------|-------------------------------------|
| Add task         | Type + click Add (or press Enter)   |
| Complete task    | Click the ⬜ checkbox               |
| Edit task        | Click ✏️, type, press Enter or 💾   |
| Delete task      | Click 🗑️ and confirm               |
| Filter tasks     | All / Active / Done tabs            |
| Remaining count  | Auto-updates at the bottom          |
| JSON API         | GET /api/todos returns all todos    |

---

## 🔑 Key Concepts Learned

1. **Flask routing** — `@app.route()` maps URLs to Python functions
2. **SQLite** — lightweight database, no server needed
3. **Jinja2 templates** — Python variables inside HTML `{{ }}`
4. **HTML forms** — POST data to the server
5. **Fetch API** — JavaScript talking to Python backend
6. **REST-style routes** — `/add`, `/toggle/<id>`, `/delete/<id>`

---

## 🛠️ Extend It

- Add user login with `flask-login`
- Add due dates
- Deploy to the web with Render or Railway (free tier)
