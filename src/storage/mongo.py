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

    def get_competitions(
        self,
        date_from: str = "",
        date_to: str = "",
        position: int = 0,
        level: str = "",
    ) -> Iterable[Competition]:
        query = {}

        if date_from:
            date_from_dt = datetime.strptime(date_from, "%d.%m.%Y")
            query["date"] = {"$gte": date_from_dt}

        if date_to:
            date_to_dt = datetime.strptime(date_to, "%d.%m.%Y")
            if "date" in query:
                query["date"] = query["date"] | {"$lte": date_to_dt}
            else:
                query["date"] = {"$lte": date_to_dt}

        if position != 0:
            query["position"] = position

        if level:
            query["level"] = level

        competitions = []

        records = self.competitions.find(query)
        for record in records:
            competition = Competition.parse_obj(record)
            competitions.append(competition)

        return competitions

    def save_competitions(self, competitons: Iterable[Competition]):
        records = [item.dict() for item in competitons]
        result = self.competitions.insert_many(records)

    def clean_db(self):
        self.competitions.delete_many({})
