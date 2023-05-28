from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Competition(BaseModel):
    student_id: str
    student_name: str
    student_sex: Optional[str]
    institute: str
    group: str
    sport: Optional[str]
    date: Optional[datetime]
    level: Optional[str]
    name: Optional[str]
    position: Optional[int]
    course: Optional[int]
    count_participation: Optional[int]
