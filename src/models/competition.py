from datetime import datetime

from src.models.student import Student


class Competition(Student):
    sport: str
    date: datetime
    level: str
    name: str
    position: int
    course: int
