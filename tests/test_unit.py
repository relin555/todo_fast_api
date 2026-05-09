from src.todo.schemas import TaskCreate, TaskUpdate
from src.todo.utils import generate_short_code
def test_create_task_schema():
    task = TaskCreate(
        title="Test task",
        description="Some description",
        status="new",
        priority=5
    )

    assert task.title == "Test task"
    assert task.description == "Some description"
    assert task.status == "new"
    assert task.priority == 5

def test_empty_update_model():
    task = TaskUpdate()
    assert task.model_dump(exclude_unset=True) == {}


def test_update_model():
    task = TaskUpdate(title="New title")
    assert task.model_dump(exclude_unset=True) == {
        "title": "New title"
    }
    
def test_generate_short_code_length():
    code = generate_short_code()
    assert len(code) == 6

def test_generate_short_code_unique():
    codes = {generate_short_code() for _ in range(1000)}
    assert len(codes) == 1000