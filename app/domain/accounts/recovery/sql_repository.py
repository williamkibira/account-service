from datetime import datetime
from typing import Optional

from sqlalchemy.engine import Result
from sqlalchemy.exc import DatabaseError

from app.core.database.connection import DataSource
from app.core.logging.loggers import LoggerMixin
from app.domain.accounts.recovery.repository import RecoveryRepository


class SQLRecoveryRepository(RecoveryRepository, LoggerMixin):

    def __init__(self, data_source: DataSource):
        self.__data_source = data_source

    def add_request(self, reference: str, otp: str, due_date: datetime, email_address: str) -> bool:
        try:
            with self.__data_source.session as session:
                sql: str = "INSERT INTO recovery_tb(reference, otp, due_date, user_id) " \
                           "VALUES(:reference, :otp, :due_date, " \
                           "(SELECT id FROM user_tb WHERE email_address=:email_address))"
                session.execute(
                    statement=sql,
                    params={'reference': reference, 'otp': otp, 'due_date': due_date, 'email_address': email_address})
                return True
        except DatabaseError as e:
            self._error("QUERY EXECUTION FAILED: {}".format(e))
            return False

    def fetch_user_identifier(self, reference: str) -> Optional[str]:
        try:
            with self.__data_source.session as session:
                sql: str = "SELECT u.identifier FROM user_tb AS u " \
                           "INNER JOIN recovery_tb AS r ON r.user_id=u.id " \
                           "WHERE r.reference = :reference AND r.due_date > :current_date"
                results: Result = session.execute(statement=sql, params={
                    'reference': reference,
                    'current_date': datetime.utcnow()
                })
                if results is None:
                    return None
                return results.one()["identifier"]
        except DatabaseError as e:
            self._error("QUERY EXECUTION FAILED: {}".format(e))
            return False
