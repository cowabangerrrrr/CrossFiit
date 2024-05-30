from dataclasses import dataclass
from flask_login import UserMixin


@dataclass
class User(UserMixin):
    id: int
    email: str
