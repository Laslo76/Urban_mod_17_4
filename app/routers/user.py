from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import User
from sqlalchemy import insert, select, update, delete
from app.schemas import CreateUser, UpdateUser

from slugify import slugify


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    if users is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no user'
        )
    return users


@router.get('/{user_id}')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found"'
        )
    return user


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], user_crt: CreateUser):
    try:
        db.execute(insert(User).values(username=user_crt.username,
                                       firstname=user_crt.firstname,
                                       lastname=user_crt.lastname,
                                       age=user_crt.age,
                                       slug=slugify(user_crt.username)))
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
async def update_user(db: Annotated[Session, Depends(get_db)],
                      user_id: int,
                      user_upd: UpdateUser):
    user_update = db.scalar(select(User).where(User.id == user_id))
    if user_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    db.execute(update(User).where(User.id == user_id).values(username=user_upd.username,
                                                             firstname=user_upd.firstname,
                                                             lastname=user_upd.lastname,
                                                             age=user_upd.age,
                                                             slug=slugify(user_upd.username)))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful!'
    }


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)],
                      user_id: int):
    user_update = db.scalar(select(User).where(User.id == user_id))
    if user_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User deleted is successful!'
    }
