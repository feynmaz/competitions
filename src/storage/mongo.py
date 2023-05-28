from datetime import datetime
from typing import Iterable, List

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.models.competition import Competition


class MongoAdapter:
    def __init__(self):
        uri = "mongodb+srv://competitionsdb:2CnKp7PAWeup2MzQ@cluster0.fhmjsxn.mongodb.net/?retryWrites=true&w=majority"

        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi("1"))
        client.admin.command("ping")

        self.competitions = client.competitions.competitions

    def get_competitions(self) -> Iterable[Competition]:
        competitions = []

        records = self.competitions.find(filter)
        for record in records:
            competition = Competition.parse_obj(record)
            competitions.append(competition)

        return competitions

    def get_filtered(
        self,
        date_from: str = "",
        date_to: str = "",
        position: int = 0,
        level: str = "",
    ):
        filter = {}

        if date_from:
            date_from_dt = datetime.strptime(date_from, "%d.%m.%Y")
            filter["date"] = {"$gte": date_from_dt}

        if date_to:
            date_to_dt = datetime.strptime(date_to, "%d.%m.%Y")
            if "date" in filter:
                filter["date"] = filter["date"] | {"$lte": date_to_dt}
            else:
                filter["date"] = {"$lte": date_to_dt}

        if position != 0:
            filter["position"] = position

        if level:
            filter["level"] = level

        pipeline = [
            # {"$match": filter},
            {
                "$group": {
                    "_id": {
                        "student_id": "$student_id",
                        "student_name": "$student_name",
                        "student_sex": "$student_sex",
                        "institute": "$institute",
                        "group": "$group",
                        "course": "$course",
                    },
                    "count": {"$sum": 1},
                },
            },
        ]
        records = self.competitions.aggregate(pipeline)

        competitions = []
        for record in records:
            fields = record.get("_id")
            competition = Competition(
                student_id=fields["student_id"],
                student_name=fields["student_name"],
                student_sex=fields["student_sex"],
                institute=fields["institute"],
                group=fields["group"],
                course=fields["course"],
                count_participation=record["count"],
            )
            competitions.append(competition)

        return competitions

    def save_competitions(self, competitons: Iterable[Competition]):
        records = [item.dict() for item in competitons]
        result = self.competitions.insert_many(records)

    def clean_db(self):
        self.competitions.delete_many({})
