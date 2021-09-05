from typing import NamedTuple


class PasswordReset(NamedTuple):
    reference: str
    otp: str
    email: str


class AccountDetails(NamedTuple):
    email: str
    first_name: str
    last_name: str
