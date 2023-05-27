from typing import Optional
from pydantic import BaseModel
from datetime import datetime


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
    position: str
    course: Optional[int]
