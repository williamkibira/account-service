from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship

from app.core.database.base import BaseModel
from app.domain.acm.roles.models import Role


class User(BaseModel):
    __tablename__ = 'user_tb'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, default=func.now())
    roles = relationship(
        Role,
        secondary='user_roles'
    )


class UserRoles(Base):
    __tablename__ = 'user_roles'
    user_id = Column(Integer, ForeignKey('user_tb.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('role_tb.id'), primary_key=True)
