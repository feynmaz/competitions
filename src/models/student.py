from pydantic import BaseModel


class Student(BaseModel):
    student_id: str
    student_name: str
    student_sex: str
    institute: str
    group: str
    course: int
