from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database.base import BaseModel


class Role(BaseModel):
    __tablename__ = 'role_tb'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    users = relationship(
        'User',
        secondary='user_roles'
    )
