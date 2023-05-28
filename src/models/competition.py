from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Competition(BaseModel):
    student_id: str
    student_name: str
    student_sex: Optional[str]
    institute: str
    group: str
    sport: str
    date: datetime
    level: str
    name: str
    position: int
    course: Optional[int]
