import hashlib

import pandas as pd
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from src.models.competition import Competition
from src.storage.mongo import MongoAdapter

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


@app.get("/clean_db")
def clean_db():
    mongo.clean_db()
    return RedirectResponse(url="/")
