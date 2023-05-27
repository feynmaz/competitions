from fastapi import FastAPI, Request
from fastapi import FastAPI, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import pandas as pd
from src.models.competition import Competition
import hashlib

from src.storage.mongo import MongoAdapter

months = {
    "январь": 1,
    "февраль": 2,
    "март": 3,
    "апрель": 4,
    "май": 5,
    "июнь": 6,
    "июль": 7,
    "август": 8,
    "сентябрь": 9,
    "октябрь": 10,
    "ноябрь": 11,
    "декабрь": 12,
}

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")

mongo = MongoAdapter()


@app.get("/")
def index(request: Request):
    competitions = mongo.get_competitions()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "competitions": competitions,
        },
    )


@app.post("/")
def upload(file: UploadFile = File(...)):
    contents = file.file.read()
    df = pd.read_excel(io=contents)

    competitions = []
    for _, row in df.iterrows():
        record = row.to_dict()

        student_name = record["ФИО"]
        date = record["Дата"]

        competition = Competition(
            student_id=hashlib.sha256(student_name.encode()).hexdigest(),
            student_name=student_name,
            student_sex=record["Пол"],
            institute=record["Институт"],
            group=record["Группа"],
            date=date,
            sport=record["Вид спорта"],
            level=record["Уровень соревнований"],
            name=record["Название соревнований"],
            position=record["Место"],
            course=record["Курс"],
        )
        competitions.append(competition)

    mongo.save_competitions(competitions)
    return RedirectResponse(url="/", status_code=302)
