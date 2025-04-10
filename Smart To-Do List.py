import heapq
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
import numpy as np

tasks = []  # Min-heap for priority queue
scaler = MinMaxScaler(feature_range=(1, 10))  # Normalize priority scores

def calculate_priority(due_date, importance, effort):
    """Calculate task priority using AI-based normalization."""
    days_left = (due_date - datetime.now()).days
    raw_scores = np.array([[importance, -effort, -days_left]])
    normalized_scores = scaler.fit_transform(raw_scores)
    return sum(normalized_scores[0])  # Higher score means higher priority

def add_task(title, due_date_str, importance, effort):
    """Add a new task with AI prioritization."""
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
    priority = calculate_priority(due_date, importance, effort)
    heapq.heappush(tasks, (-priority, title, due_date_str))  # Max-Heap Simulation
    print(f"Task '{title}' added with AI-prioritized score {priority:.2f}.")

def get_tasks():
    """Display sorted tasks based on AI prioritization."""
    sorted_tasks = sorted(tasks, reverse=True)
    print("\nTo-Do List (AI Prioritized):")
    for _, title, due_date in sorted_tasks:
        print(f"- {title} (Due: {due_date})")

def mark_task_done(title):
    """Remove a completed task."""
    global tasks
    tasks = [t for t in tasks if t[1] != title]
    heapq.heapify(tasks)
    print(f"Task '{title}' marked as done.")

# Example Usage
add_task("Complete Data Report", "2025-04-15", importance=5, effort=3)
add_task("Prepare for Meeting", "2025-04-12", importance=4, effort=2)
add_task("Buy Groceries", "2025-04-10", importance=2, effort=1)
get_tasks()
mark_task_done("Buy Groceries")
get_tasks()
