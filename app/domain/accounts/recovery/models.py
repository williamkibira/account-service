from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from app.core.database.base import BaseModel
from app.domain.acm.users.models import User


class RecoveryOrder(BaseModel):
    __tablename__ = 'recovery_tb'
    id = Column('id', BigInteger, primary_key=True)
    reference = Column('reference', String)
    otp = Column('otp', String)
    due_date = Column('due_date', DateTime, nullable=False)
    user_id = Column("user_id", BigInteger, ForeignKey(User.id), nullable=False, index=True)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    index = Column('idx', Integer)
    user = relationship(User, foreign_keys='RecoveryOrder.user_id')
