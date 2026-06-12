from flask import Flask, render_template, request, redirect
from apscheduler.schedulers.background import BackgroundScheduler
from database import get_db, init_db

app = Flask(__name__)
with app.app_context():
    init_db()



@app.route("/")
def index():
    conn = get_db()
    cursor = conn.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    conn.close()
    return render_template("index.html", todos=todos)

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    if task:
        conn = get_db()
        conn.execute("INSERT INTO todos (title) VALUES (?)", (task,))
        conn.commit()
        conn.close()
        return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM todos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

def reset_todos():
    conn = get_db()
    conn.execute("DELETE FROM todos")
    conn.commit()
    conn.close()
scheduler = BackgroundScheduler()
scheduler.add_job(reset_todos, 'cron', hour=3, minute=0)
scheduler.start()
    
if __name__ == "__main__":
    app.run(debug=True)

