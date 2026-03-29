from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

from db import get_db
from ai_assistant import chat_response, suggest_best_task

from dotenv import load_dotenv

def make_id(id_str):
    try:
        return ObjectId(id_str)
    except Exception:
        return id_str

load_dotenv()
app = Flask(__name__)
# Secret key for session management
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-1234")

# Initialize DB
db = get_db()
if db is not None:
    users_collection = db["users"]
    tasks_collection = db["tasks"]
else:
    users_collection = None
    tasks_collection = None

@app.before_request
def check_db():
    if db is None and request.endpoint != 'static':
        return "<h1>Database Error</h1><p>MongoDB is not connected. Please check your .env file and restart the server.</p>", 500

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

# Authentication Routes
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Check if user already exists
        if users_collection.find_one({"email": email}):
            flash("Email address already exists", "error")
            return redirect(url_for("signup"))
            
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        user_id = users_collection.insert_one({
            "email": email,
            "password": hashed_password
        }).inserted_id
        
        session["user_id"] = str(user_id)
        return redirect(url_for("dashboard"))
        
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = users_collection.find_one({"email": email})
        
        if not user or not check_password_hash(user["password"], password):
            flash("Please check your login details and try again.", "error")
            return redirect(url_for("login"))
            
        session["user_id"] = str(user["_id"])
        return redirect(url_for("dashboard"))
        
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))

# Main Application Routes
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    user_id = session["user_id"]
    # Fetch tasks for correct user
    db_tasks = list(tasks_collection.find({"user_id": user_id}))
    
    # Process tasks for template
    tasks = []
    for t in db_tasks:
        t["_id"] = str(t["_id"]) # Convert ObjectId to string
        tasks.append(t)
        
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.get("completed", False)])
    pending_tasks = total_tasks - completed_tasks
    
    # Get AI recommendation
    best_task = suggest_best_task(tasks)
    
    return render_template("dashboard.html", 
                           tasks=tasks, 
                           total=total_tasks, 
                           completed=completed_tasks, 
                           pending=pending_tasks,
                           ai_suggestion=best_task)

@app.route("/add_task", methods=["POST"])
def add_task():
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    title = request.form.get("title")
    description = request.form.get("description")
    deadline = request.form.get("deadline")
    priority = request.form.get("priority")
    
    tasks_collection.insert_one({
        "user_id": session["user_id"],
        "title": title,
        "description": description,
        "deadline": deadline,
        "priority": priority,
        "completed": False
    })
    
    flash("Task added successfully!", "success")
    return redirect(url_for("dashboard"))

@app.route("/complete_task/<task_id>")
def complete_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    tasks_collection.update_one(
        {"_id": make_id(task_id), "user_id": session["user_id"]},
        {"$set": {"completed": True}}
    )
    return redirect(url_for("dashboard"))

@app.route("/delete_task/<task_id>")
def delete_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    tasks_collection.delete_one({"_id": make_id(task_id), "user_id": session["user_id"]})
    return redirect(url_for("dashboard"))

# API Route for Chatbot
@app.route("/api/chat", methods=["POST"])
def chat_api():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    data = request.json
    query = data.get("message", "")
    
    # Fetch user's current tasks to give context
    user_id = session["user_id"]
    db_tasks = list(tasks_collection.find({"user_id": user_id}))
    
    # Get intelligent response
    response_text = chat_response(query, db_tasks)
    
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)
