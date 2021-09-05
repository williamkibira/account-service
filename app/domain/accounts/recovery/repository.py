import abc
from datetime import datetime
from typing import Optional


class RecoveryRepository(abc.ABC):
    @abc.abstractmethod
    def add_request(self, reference: str, otp: str, due_date: datetime, email_address: str) -> bool:
        pass

    @abc.abstractmethod
    def fetch_user_identifier(self, reference: str) -> Optional[str]:
        pass
