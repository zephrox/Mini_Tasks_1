import json
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
JSON_FILE = "tasks.json"

def read_tasks():
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def write_tasks(tasks):
    with open(JSON_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task.get("id", 0) for task in tasks) + 1

@app.route("/")
def index():
    filter_status = request.args.get("status", "All")
    tasks = read_tasks()
    
    if filter_status and filter_status != "All":
        filtered_tasks = [t for t in tasks if t.get("status") == filter_status]
    else:
        filtered_tasks = tasks
        
    def sort_key(task):
        status_order = 2 if task.get("status") == "Completed" else 1
        deadline = task.get("deadline", "")
        deadline_str = deadline if deadline else "9999-99-99"
        return (status_order, deadline_str, -task.get("id", 0))

    filtered_tasks.sort(key=sort_key)

    return render_template("index.html", tasks=filtered_tasks, current_filter=filter_status)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    deadline = request.form.get("deadline", "").strip()
    priority = request.form.get("priority", "Medium")

    if title:
        tasks = read_tasks()
        new_task = {
            "id": get_next_id(tasks),
            "title": title,
            "description": description,
            "deadline": deadline,
            "priority": priority,
            "status": "Pending",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        tasks.append(new_task)
        write_tasks(tasks)

    return redirect(url_for("index"))

@app.route("/update-status/<int:task_id>", methods=["POST"])
def update_status(task_id):
    new_status = request.form.get("status")
    if new_status in ["Pending", "In Progress", "Completed"]:
        tasks = read_tasks()
        for task in tasks:
            if task.get("id") == task_id:
                task["status"] = new_status
                break
        write_tasks(tasks)
    return redirect(request.referrer or url_for("index"))

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    tasks = read_tasks()
    task = next((t for t in tasks if t.get("id") == task_id), None)
    
    if task is None:
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        deadline = request.form.get("deadline", "").strip()
        priority = request.form.get("priority", "Medium")
        status = request.form.get("status", "Pending")

        if title:
            task["title"] = title
            task["description"] = description
            task["deadline"] = deadline
            task["priority"] = priority
            task["status"] = status
            write_tasks(tasks)
        return redirect(url_for("index"))

    return render_template("edit.html", task=task)

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    tasks = read_tasks()
    tasks = [t for t in tasks if t.get("id") != task_id]
    write_tasks(tasks)
    return redirect(url_for("index"))

if __name__ == "__main__":
    if not os.path.exists(JSON_FILE):
        write_tasks([])
    app.run(debug=True, port=5000)
