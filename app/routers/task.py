from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import *
from sqlalchemy import insert, select, update, delete
from app.schemas import CreateTask, UpdateTask

from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/")
async def all_tasks_(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    if tasks is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no task'
        )
    return tasks


@router.get('/{task_id}')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task_by_ = db.scalar(select(Task).where(Task.id == task_id))
    if not task_by_:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
    return task_by_


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], task_crt: CreateTask, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    try:
        db.execute(insert(Task).values(title=task_crt.title,
                                       content=task_crt.content,
                                       priority=task_crt.priority,
                                       user_id=user_id,
                                       slug=slugify(task_crt.title)))

        db.commit()
    except Exception:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='recording error'
        )
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)],
                      task_id: int,
                      task_upd: UpdateTask):
    task_update = db.scalar(select(Task).where(Task.id == task_id))
    if task_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    db.execute(update(Task).where(Task.id == task_id).values(title=task_upd.title,
                                                             content=task_upd.content,
                                                             priority=task_upd.priority,
                                                             completed=task_upd.completed,
                                                             slug=slugify(task_upd.title)))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful!'
    }


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)],
                      task_id: int):
    task_del = db.scalar(select(Task).where(Task.id == task_id))
    if task_del is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task deleted is successful!'
    }
