import hashlib

import pandas as pd
from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import select_autoescape
from sanic import redirect
from sanic import Request
from sanic import Sanic
from sanic import text
from sanic_ext import render

from src.models.competition import Competition
from src.storage.mongo import MongoAdapter


jinja_env = Environment(
    loader=PackageLoader("src"),
    autoescape=select_autoescape(),
    enable_async=True,
)

app = Sanic("SIBADI_competitions")

app.static(
    uri="/static",
    file_or_directory="src/static",
    name="static",
    directory_view=True,
)

mongo = MongoAdapter()


@app.get("/")
async def index(request: Request):
    competitions = mongo.get_competitions()
    return await render(
        template_name=jinja_env.get_template("index.html"),
        context={
            "request": request,
            "competitions": competitions,
        },
    )


@app.post("/")
async def upload(request: Request):
    upload_file = request.files.get("file")
    if not upload_file or not upload_file.body:
        return text(body="No file uploaded", status=400)

    df = pd.read_excel(io=upload_file.body)

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
            position=record["Место"] if record["Место"] else 0,
            course=record["Курс"],
        )
        competitions.append(competition)

    mongo.save_competitions(competitions)
    return redirect(to="/")


@app.get("/clean_db")
async def clean_db(request: Request):
    mongo.clean_db()
    return redirect(to="/")


@app.get("/report")
async def get_report(request: Request):
    args = dict(request.args)

    date_from: str = args.get("date_from", "")
    date_to: str = args.get("date_to", "")
    position: list[str] = args.get("position", [])
    level: list[str] = args.get("level", [])

    student_infos = mongo.get_filtered(
        date_from=date_from,
        date_to=date_to,
        position=position,
        level=level,
    )
    return await render(
        template_name=jinja_env.get_template("filtered.html"),
        context={
            "request": request,
            "student_infos": student_infos,
        },
    )
