# TaskMaster AI: Cloud-Based Task Management Application

A full-stack AI-powered task management web application built with Python Flask, MongoDB Atlas, HTML, and vanilla CSS. This project leverages rule-based heuristic "AI" logic to intelligently analyze tasks based on their deadlines and priority levels, providing users with dynamic recommendations on what to tackle next.

## Core Features
- **User Authentication:** Secure Signup/Login system with password hashing (`werkzeug.security`).
- **Task Management:** Complete CRUD (Create, Read, Update, Delete) for tasks with `priority`, `deadline`, and `description`.
- **MongoDB Atlas Integration:** All data securely synchronized to an online cloud database instead of local SQL.
- **Smart Priority AI:** Automatically analyzes pending tasks, weighing priority level vs. deadline proximity to suggest the most critical immediate task.
- **Smart Assistant Chatbot:** A built-in virtual assistant that contextually understands a user's task list to suggest actions.
- **Beautiful UI:** A custom-designed modern SaaS interface using glassmorphism, responsive grid layouts, and smooth animations without heavy CSS frameworks.

---

## 🚀 Setup & Local Installation

### Prerequisites
- Python 3.9+ installed
- A free MongoDB Atlas Account ([Register here](https://www.mongodb.com/cloud/atlas/register))

### 1. Clone & Install
```bash
git clone <your-repo-link>
cd taskmaster-ai
pip install -r requirements.txt
```

### 2. Configure MongoDB Atlas
1. Create a cluster on MongoDB Atlas.
2. Under "Database Access", create a Database User with a password.
3. Under "Network Access", add `0.0.0.0/0` to allow connections from anywhere.
4. Go to "Databases" -> "Connect" -> "Drivers" (Python) and copy your connection string.

### 3. Environment Variables
Create a file named `.env` in the root directory and add the following:
```ini
SECRET_KEY=your_secure_random_key_here
MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority
```

### 4. Run the Application
```bash
python app.py
```
Open `http://localhost:5000` in your browser.

---

## 🌍 Deployment Guide (Render)

This application is ready to be deployed on platforms like **Render** or **Railway**. Render is recommended for beginners.

1. **Push to GitHub**: Make sure your project is pushed to a fresh GitHub repository. Do NOT commit the `.env` file.
2. **Sign up on Render**: Go to [Render](https://render.com/) and connect your GitHub account.
3. **Create a New Web Service**: Select "Web Service" and choose your repository.
4. **Configuration Settings**:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app` (Gunicorn is included in the requirements).
5. **Add Environment Variables**: Under the "Environment" tab on Render, add:
   - `MONGO_URI`: (Paste your Atlas connection string here)
   - `SECRET_KEY`: (Any random string for session security)
6. **Deploy**: Click "Create Web Service". The app will be built and you will receive a free `xxxxx.onrender.com` public URL!

---

## 🎤 Viva Explanation (For Project Submissions)

**Q: What is this project and what problem does it solve?**
**A:** This is "TaskMaster AI", a cloud-based task management web application. It solves the problem of "decision fatigue" that users face when having too many tasks by intelligently analyzing task deadlines and priority levels, and automatically suggesting what task the user should focus on first.

**Q: What technologies did you use for the frontend and backend?**
**A:** The frontend uses HTML5 and modern, responsive vanilla CSS without external frameworks (like Tailwind or Bootstrap) to ensure lightweight, custom control. The backend is built using Python with the Flask framework, primarily because Flask is modular, lightweight, and excellent for rapid API development.

**Q: Why MongoDB Atlas instead of MySQL?**
**A:** I chose MongoDB Atlas because it is a NoSQL cloud database. Task data doesn't necessarily have a rigid schema—some tasks have descriptions, some don't. MongoDB stores data in flexible JSON-like documents (BSON), matching perfectly with Python dictionaries, and since it is hosted on Atlas, the data persists no matter where the app is deployed.

**Q: How does the "AI" component work?**
**A:** Using a heuristic rule-based AI approach, the backend application dynamically calculates a score for each pending task. "High" priority tasks receive heavy score weighting, which is dynamically compounded by checking the exact number of days remaining until the deadline. Sort functions bubble the most critical task to the surface to populate the AI Recommendation Banner. Additionally, a Smart Assistant chatbot parses string inputs to formulate user-specific advice using their real-time task context.
