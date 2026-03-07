from dataclasses import dataclass


@dataclass
class User:
    id: int


def get_current_user() -> User:
    return User(id=1)