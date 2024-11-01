from app.backend.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = "tasks"
    __table_arg__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    slug = Column(String, unique=True, index=True)


#from sqlalchemy.schema import CreateTable
#print(CreateTable(Task.__table__))
