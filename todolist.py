# todo_app.py

import os
import json
import datetime
from typing import List, Dict, Any, Optional
import uuid
import sys
from enum import Enum

# Define task priority and status as enums
class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Status(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Task:
    """Represents a task in the todo list"""
   
    def __init__(self,
                 title: str,
                 description: str = "",
                 due_date: Optional[str] = None,
                 priority: Priority = Priority.MEDIUM,
                 status: Status = Status.TODO):
        """Initialize a new task"""
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.created_at = datetime.datetime.now().isoformat()
        self.updated_at = self.created_at
   
    def update(self,
               title: Optional[str] = None,
               description: Optional[str] = None,
               due_date: Optional[str] = None,
               priority: Optional[Priority] = None,
               status: Optional[Status] = None) -> None:
        """Update task properties"""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if due_date is not None:
            self.due_date = due_date
        if priority is not None:
            self.priority = priority
        if status is not None:
            self.status = status
        self.updated_at = datetime.datetime.now().isoformat()
   
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for storage"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
   
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create a task from dictionary data"""
        task = cls(
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date"),
            priority=Priority(data.get("priority", "medium")),
            status=Status(data.get("status", "todo"))
        )
        task.id = data["id"]
        task.created_at = data["created_at"]
        task.updated_at = data["updated_at"]
        return task
   
    def __str__(self) -> str:
        """String representation of the task"""
        due_str = f" (Due: {self.due_date})" if self.due_date else ""
        return f"[{self.priority.value.upper()}] {self.title}{due_str} - {self.status.value}"


class TaskManager:
    """Manages tasks in the todo list"""
   
    def __init__(self, storage_file: str = "tasks.json"):
        """Initialize the task manager"""
        self.storage_file = storage_file
        self.tasks: List[Task] = []
        self.load_tasks()
   
    def load_tasks(self) -> None:
        """Load tasks from storage file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    tasks_data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in tasks_data]
            except Exception as e:
                print(f"Error loading tasks: {e}")
                self.tasks = []
   
    def save_tasks(self) -> None:
        """Save tasks to storage file"""
        try:
            with open(self.storage_file, 'w') as f:
                tasks_data = [task.to_dict() for task in self.tasks]
                json.dump(tasks_data, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
   
    def add_task(self, task: Task) -> None:
        """Add a new task"""
        self.tasks.append(task)
        self.save_tasks()
   
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
   
    def update_task(self, task_id: str, **kwargs) -> bool:
        """Update a task by ID"""
        task = self.get_task(task_id)
        if task:
            # Convert string values to enum types if needed
            if "priority" in kwargs and isinstance(kwargs["priority"], str):
                kwargs["priority"] = Priority(kwargs["priority"])
            if "status" in kwargs and isinstance(kwargs["status"], str):
                kwargs["status"] = Status(kwargs["status"])
               
            task.update(**kwargs)
            self.save_tasks()
            return True
        return False
   
    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID"""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True
        return False
   
    def list_tasks(self, status: Optional[Status] = None,
                  priority: Optional[Priority] = None,
                  sort_by: str = "created_at") -> List[Task]:
        """List tasks with optional filtering and sorting"""
        filtered_tasks = self.tasks
       
        # Filter by status
        if status:
            filtered_tasks = [task for task in filtered_tasks if task.status == status]
       
        # Filter by priority
        if priority:
            filtered_tasks = [task for task in filtered_tasks if task.priority == priority]
       
        # Sort tasks
        if sort_by == "priority":
            # Sort by priority (HIGH > MEDIUM > LOW)
            priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
            filtered_tasks.sort(key=lambda task: priority_order[task.priority])
        elif sort_by == "due_date":
            # Sort by due date (None values at the end)
            filtered_tasks.sort(key=lambda task: task.due_date or "9999-12-31")
        else:  # Default sort by created_at
            filtered_tasks.sort(key=lambda task: task.created_at)
       
        return filtered_tasks


class TodoApp:
    """Command-line interface for the todo list application"""
   
    def __init__(self):
        """Initialize the todo app"""
        self.task_manager = TaskManager()
        self.commands = {
            "add": self.add_task,
            "list": self.list_tasks,
            "update": self.update_task,
            "delete": self.delete_task,
            "help": self.show_help,
            "exit": self.exit_app
        }
   
    def show_help(self) -> None:
        """Show help information"""
        print("\n===== Todo List App Help =====")
        print("Available commands:")
        print("  add - Add a new task")
        print("  list [all|todo|in_progress|done] [priority] [sort_by] - List tasks")
        print("  update <task_id> - Update a task")
        print("  delete <task_id> - Delete a task")
        print("  help - Show this help message")
        print("  exit - Exit the application")
        print("=============================\n")
   
    def add_task(self, *args) -> None:
        """Add a new task"""
        title = input("Task title: ")
        if not title:
            print("Task title cannot be empty.")
            return
       
        description = input("Description (optional): ")
       
        due_date = input("Due date (YYYY-MM-DD) (optional): ")
        if due_date:
            try:
                # Validate date format
                datetime.datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Using no due date.")
                due_date = None
       
        priority_input = input("Priority (low/medium/high) [medium]: ").lower()
        try:
            priority = Priority(priority_input) if priority_input else Priority.MEDIUM
        except ValueError:
            print("Invalid priority. Using medium.")
            priority = Priority.MEDIUM
       
        task = Task(title, description, due_date, priority)
        self.task_manager.add_task(task)
        print(f"Task added: {task}")
   
    def list_tasks(self, *args) -> None:
        """List tasks with optional filtering"""
        status_filter = None
        priority_filter = None
        sort_by = "created_at"
       
        # Parse arguments
        for arg in args:
            if arg in ["all", "todo", "in_progress", "done"]:
                status_filter = None if arg == "all" else Status(arg)
            elif arg in ["low", "medium", "high"]:
                priority_filter = Priority(arg)
            elif arg in ["created_at", "priority", "due_date"]:
                sort_by = arg
       
        tasks = self.task_manager.list_tasks(status_filter, priority_filter, sort_by)
       
        if not tasks:
            print("No tasks found.")
            return
       
        print("\n===== Tasks =====")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")
            print(f"   ID: {task.id}")
            if task.description:
                print(f"   Description: {task.description}")
            print()
        print("=================\n")
   
    def update_task(self, *args) -> None:
        """Update a task"""
        if not args:
            print("Please provide a task ID to update.")
            return
       
        task_id = args[0]
        task = self.task_manager.get_task(task_id)
       
        if not task:
            print(f"Task with ID {task_id} not found.")
            return
       
        print(f"Updating task: {task}")
       
        title = input(f"New title [{task.title}]: ")
        description = input(f"New description [{task.description}]: ")
        due_date = input(f"New due date [{task.due_date or ''}]: ")
        priority_input = input(f"New priority (low/medium/high) [{task.priority.value}]: ").lower()
        status_input = input(f"New status (todo/in_progress/done) [{task.status.value}]: ").lower()
       
        # Prepare update data
        update_data = {}
        if title:
            update_data["title"] = title
        if description:
            update_data["description"] = description
        if due_date:
            update_data["due_date"] = due_date
        if priority_input:
            try:
                update_data["priority"] = Priority(priority_input)
            except ValueError:
                print("Invalid priority. Keeping current value.")
        if status_input:
            try:
                update_data["status"] = Status(status_input)
            except ValueError:
                print("Invalid status. Keeping current value.")
       
        if update_data:
            self.task_manager.update_task(task_id, **update_data)
            print("Task updated successfully.")
        else:
            print("No changes made.")
   
    def delete_task(self, *args) -> None:
        """Delete a task"""
        if not args:
            print("Please provide a task ID to delete.")
            return
       
        task_id = args[0]
        task = self.task_manager.get_task(task_id)
       
        if not task:
            print(f"Task with ID {task_id} not found.")
            return
       
        confirm = input(f"Are you sure you want to delete task '{task.title}'? (y/n): ")
        if confirm.lower() == 'y':
            self.task_manager.delete_task(task_id)
            print("Task deleted successfully.")
        else:
            print("Deletion cancelled.")
   
    def exit_app(self, *args) -> None:
        """Exit the application"""
        print("Goodbye!")
        sys.exit(0)
   
    def run(self) -> None:
        """Run the application main loop"""
        print("Welcome to the Todo List App!")
        print("Type 'help' for available commands.")
       
        while True:
            try:
                user_input = input("\nEnter command: ").strip()
                if not user_input:
                    continue
               
                parts = user_input.split()
                command = parts[0].lower()
                args = parts[1:]
               
                if command in self.commands:
                    self.commands[command](*args)
                else:
                    print(f"Unknown command: {command}")
                    print("Type 'help' for available commands.")
           
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    app = TodoApp()
    app.run()
