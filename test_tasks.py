import json
import pytest
from tasks import Task, TaskManager

class TestTaskManager:
    def setup_method(self):
        self.manager = TaskManager()
        self.manager.tasks = []  # Очистка задач перед каждым тестом

    def test_add_task(self):
        task = Task("New Task", "Description", "Category", "2024-12-31", "high")
        self.manager.add_task(task.title, task.description, task.category, task.due_date, task.priority)  # Передача параметров отдельно
        assert len(self.manager.tasks) == 1, "Задача должна быть добавлена"

    def test_prevent_duplicate_tasks(self):
        task1 = Task("Duplicate Task", "Description", "Category", "2023-12-31", "high")
        task2 = Task("Duplicate Task", "Description", "Category", "2023-12-31", "high")
        self.manager.add_task(task1.title, task1.description, task1.category, task1.due_date, task1.priority)
        with pytest.raises(ValueError, match="Задача с таким названием уже существует."):
            self.manager.add_task(task2.title, task2.description, task2.category, task2.due_date, task2.priority)

    def test_unique_task_ids(self):
        task1 = Task("Task 1", "Description", "Category", "2023-12-31", "high")
        task2 = Task("Task 2", "Description", "Category", "2023-12-31", "high")
        self.manager.add_task(task1.title, task1.description, task1.category, task1.due_date, task1.priority)
        self.manager.add_task(task2.title, task2.description, task2.category, task2.due_date, task2.priority)
        assert task1.id != task2.id, "ID задач должны быть уникальными"

    def test_delete_nonexistent_task(self):
        with pytest.raises(ValueError, match="Задача не найдена"):
            self.manager.delete_task(999)  # пытаемся удалить несуществующую задачу

    def test_save_tasks(self):
        task = Task("Save Task", "Description", "Category", "2023-12-31", "high")
        self.manager.add_task(task.title, task.description, task.category, task.due_date, task.priority)
        self.manager.save_tasks()
        
        with open('data.json', 'r') as f:
            saved_tasks = json.load(f)
            assert len(saved_tasks) == 1, "Должна быть сохранена одна задача"
            assert saved_tasks[0]['title'] == "Save Task", "Сохраненная задача должна иметь правильное название"

    def test_search_tasks(self):
        task1 = Task("Search Task 1", "Description", "Work", "2023-12-31", "high")
        task2 = Task("Search Task 2", "Description", "Home", "2023-12-31", "low")
        self.manager.add_task(task1.title, task1.description, task1.category, task1.due_date, task1.priority)
        self.manager.add_task(task2.title, task2.description, task2.category, task2.due_date, task2.priority)
        
        results = self.manager.search_tasks(keyword="1")
        assert len(results) == 1, "Должна быть найдена одна задача"
        assert results[0].title == "Search Task 1", "Найдена задача должна соответствовать критерию поиска"

    def test_list_tasks(self, capsys):
        task = Task("List Task", "Description", "Category", "2023-12-31", "high")
        self.manager.add_task(task.title, task.description, task.category, task.due_date, task.priority)
        
        self.manager.list_tasks()
        captured = capsys.readouterr()
        assert "List Task" in captured.out, "Вывод должен содержать название задачи"

if __name__ == "__main__":
    pytest.main()
