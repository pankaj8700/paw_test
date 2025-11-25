from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from schemas.task import TaskCreate, TaskRead, TaskUpdate
from models.task import Task
from models.user import User, RoleEnum
from auth import get_current_user, role_required

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskRead)
def create_task(
    task_in: TaskCreate,
    session: Session = Depends(get_session),
    user: User = Depends(role_required(["admin", "manager"]))
):
    task = Task(
        title=task_in.title,
        description=task_in.description,
        assigned_to_id=task_in.assigned_to_id,
        created_by_id=user.id
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/", response_model=list[TaskRead])
def get_tasks(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    if user.role == RoleEnum.employee:
        return session.exec(
            select(Task).where(Task.assigned_to_id == user.id)
        ).all()

    return session.exec(select(Task)).all()


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    updates: TaskUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    if user.role == RoleEnum.employee:
        if task.assigned_to_id != user.id:
            raise HTTPException(403, "Not allowed")
        if updates.status:
            task.status = updates.status
        else:
            raise HTTPException(400, "Employees can update only status")
    else:
        for k, v in updates.model_dump(exclude_none=True).items():
            setattr(task, k, v)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(role_required(["admin"]))
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    session.delete(task)
    session.commit()
    return {"message": "Task deleted"}
