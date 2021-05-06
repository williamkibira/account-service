from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database.base import Base


class Role(Base):
    __tablename__ = 'role_tb'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    users = relationship(
        'User',
        secondary='user_roles'
    )
