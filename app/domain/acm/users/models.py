from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, Table
from sqlalchemy.orm import relationship

from app.core.database.base import BaseModel
from app.domain.acm.roles.models import Role

association_table = Table('user_roles', BaseModel.metadata,
                          Column('user_id', Integer, ForeignKey('user_tb.id'), primary_key=True),
                          Column('role_id', Integer, ForeignKey('role_tb.id'), primary_key=True)
                          )


class User(BaseModel):
    __tablename__ = 'user_tb'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, default=func.now())

    roles = relationship(Role,
                         secondary=association_table,
                         backref="users")
