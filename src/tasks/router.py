from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, insert, update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from src.auth.users import current_active_user
from src.auth.db import User
from src.todo.models import Task
from src.todo.schemas import TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/")
async def add_task(
    new_task: TaskCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user),
):
    statement = insert(Task).values(
        **new_task.model_dump(),
        owner_id=current_user.id
    )
    await session.execute(statement)
    await session.commit()
    return {"status": "success"}


@router.get("/")
async def get_tasks(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user),
):
    result = await session.execute(
        select(Task).where(Task.owner_id == current_user.id)
    )
    return result.scalars().all()


@router.get("/search")
async def search_tasks(
    q: str,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user),
):
    result = await session.execute(
        select(Task).where(
            Task.owner_id == current_user.id,
            or_(
                Task.title.ilike(f"%{q}%"),
                Task.description.ilike(f"%{q}%")
            )
        )
    )
    return result.scalars().all()


@router.get("/top")
async def get_top_tasks(
    limit: int = Query(3, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user),
):
    result = await session.execute(
        select(Task)
        .where(Task.owner_id == current_user.id)
        .order_by(Task.priority.desc(), Task.created_at.asc())
        .limit(limit)
    )
    return result.scalars().all()


@router.get("/{task_id}")
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user),
):
    result = await session.execute(
        select(Task).where(
            Task.id == task_id,
            Task.owner_id == current_user.id
        )
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/{task_id}")
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user),
):
    result = await session.execute(
        select(Task).where(
            Task.id == task_id,
            Task.owner_id == current_user.id
        )
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")

    statement = (
        update(Task)
        .where(Task.id == task_id, Task.owner_id == current_user.id)
        .values(**update_data)
    )
    await session.execute(statement)
    await session.commit()

    result = await session.execute(
        select(Task).where(
            Task.id == task_id,
            Task.owner_id == current_user.id
        )
    )
    updated_task = result.scalar_one()

    return updated_task


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user),
):
    result = await session.execute(
        select(Task).where(
            Task.id == task_id,
            Task.owner_id == current_user.id
        )
    )
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    statement = delete(Task).where(
        Task.id == task_id,
        Task.owner_id == current_user.id
    )
    await session.execute(statement)
    await session.commit()

    return {"status": "success"}