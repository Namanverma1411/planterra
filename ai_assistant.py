from datetime import datetime

def suggest_best_task(tasks):
    """
    Analyzes tasks based on deadline and priority to suggest the best one to do first.
    Rule: 
    1. Highest priority comes first (High > Medium > Low).
    2. Missing deadlines are pushed back.
    3. Closer deadlines come first among same priority.
    """
    if not tasks:
        return None

    priority_map = {"High": 1, "Medium": 2, "Low": 3}
    
    def score_task(task):
        priority_score = priority_map.get(task.get("priority", "Low"), 3)
        
        deadline_str = task.get("deadline", "")
        if deadline_str:
            try:
                deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                today = datetime.today().date()
                days_left = (deadline_date - today).days
                # A closer deadline gives a better (lower) score
                # Set max at 100 days so it doesn't break if distant
                days_left = min(max(days_left, -100), 100)
            except ValueError:
                days_left = 100
        else:
            days_left = 100
            
        # Priority is the most important, deadline breaks ties
        return (priority_score, days_left)

    # Filter out completed tasks first
    pending_tasks = [t for t in tasks if not t.get("completed", False)]
    if not pending_tasks:
        return None
        
    sorted_tasks = sorted(pending_tasks, key=score_task)
    return sorted_tasks[0]

def chat_response(query, tasks):
    """
    A very simple rule-based chatbot responsive to basic queries about tasks.
    """
    query = query.lower()
    pending = [t for t in tasks if not t.get("completed", False)]
    completed = [t for t in tasks if t.get("completed", False)]
    
    if "what should i do" in query or "first" in query or "suggest" in query:
        best_task = suggest_best_task(tasks)
        if best_task:
            return f"Based on your priorities and deadlines, I highly recommend starting with '{best_task['title']}'."
        return "You don't have any pending tasks right now. Time to relax!"
        
    elif "how many" in query and "task" in query:
        return f"You currently have {len(pending)} pending tasks and {len(completed)} completed tasks."
        
    elif "hello" in query or "hi" in query:
        return "Hello! I'm your AI Task Assistant. Ask me 'What should I do today?' to get started."
        
    elif "thank" in query:
        return "You're welcome! Let me know if you need anything else."
        
    else:
        return "I'm still learning! Try asking me: 'What should I do today?'"
