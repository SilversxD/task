import json
import os

TASKS_FILE = 'data.json'


class Task:
    _id_counter = 0  # Статический счетчик для генерации уникальных ID

    def __init__(self, title, description, category, due_date, priority):
        if not title:
            raise ValueError("Название задачи не может быть пустым")
        self.id = Task._id_counter
        Task._id_counter += 1
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.completed = False
        
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'due_date': self.due_date,
            'priority': self.priority,
            'completed': self.completed
        }

    def __str__(self):
        return f"{self.title} - {self.description} ({self.category}) [{self.priority}] - Due: {self.due_date}"            


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(TASKS_FILE) and os.path.getsize(TASKS_FILE) > 0:
            with open(TASKS_FILE, 'r') as f:
                try:
                    loaded_tasks = json.load(f)
                    self.tasks = []
                    for task in loaded_tasks:
                        new_task = Task(task['title'], task['description'], task['category'], task['due_date'], task['priority'])
                        new_task.id = task['id']
                        new_task.completed = task['completed']
                        self.tasks.append(new_task)
                except json.JSONDecodeError:
                    self.tasks = []  # Если JSON некорректный, просто обнуляем список задач

    def save_tasks(self):
        with open(TASKS_FILE, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f)

    def add_task(self, title, description, category, due_date, priority):
        if any(task.title == title for task in self.tasks):
            raise ValueError("Задача с таким названием уже существует.")
        task = Task(title, description, category, due_date, priority)
        task.id = len(self.tasks) + 1
        self.tasks.append(task)
        self.save_tasks()

    def complete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                self.save_tasks()
                return
        raise ValueError("Задача не найдена.")

    def delete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                return
        raise ValueError("Задача не найдена")

    def search_tasks(self, keyword=None, category=None, completed=None):
        results = self.tasks
        if keyword:
            results = [task for task in results if keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower()]
        if category:
            results = [task for task in results if task.category == category]
        if completed is not None:
            results = [task for task in results if task.completed == completed]
        return results

    def list_tasks(self):
        for task in self.tasks:
            status = "Выполнена" if task.completed else "Не выполнена"
            print(f"[{task.id}] {task.title} - {status} (Категория: {task.category}, Срок: {task.due_date}, Приоритет: {task.priority})")


def main():
    manager = TaskManager()
    while True:
        print("\nМенеджер задач")
        print("1. Просмотр задач")
        print("2. Добавить задачу")
        print("3. Завершить задачу")
        print("4. Удалить задачу")
        print("5. Поиск задач")
        print("6. Выход")
        choice = input("Выберите опцию: ")

        if choice == "1":
            manager.list_tasks()
        elif choice == "2":
            title = input("Название задачи: ")
            description = input("Описание задачи: ")
            category = input("Категория задачи: ")
            due_date = input("Срок выполнения (YYYY-MM-DD): ")
            priority = input("Приоритет (low, middle, high): ")
            manager.add_task(title, description, category, due_date, priority)
        elif choice == "3":
            task_id = int(input("ID задачи для завершения: "))
            manager.complete_task(task_id)
        elif choice == "4":
            task_id = int(input("ID задачи для удаления: "))
            manager.delete_task(task_id)
        elif choice == "5":
            keyword = input("Ключевое слово (оставьте пустым для пропуска): ")
            category = input("Категория (оставьте пустым для пропуска): ")
            completed = input("Статус (выполнена/не выполнена) (оставьте пустым для пропуска): ")
            completed = True if completed.lower() == "выполнена" else False if completed.lower() == "не выполнена" else None
            results = manager.search_tasks(keyword, category, completed)
            for task in results:
                print(f"[{task.id}] {task.title} - {'Выполнена' if task.completed else 'Не выполнена'}")
        elif choice == "6":
            break
        else:
            print("Неверный выбор, попробуйте еще раз.")


if __name__ == "__main__":
    main()
