from sqlalchemy import Column, Integer, String

from app.core.database.base import BaseModel


class Role(BaseModel):
    __tablename__ = 'role_tb'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    index = Column('idx', Integer)
