from pydantic import BaseModel


class Settings(BaseModel):
    date_format = "%d.%m.%Y"
    mongo_uri = (
        "mongodb+srv://competitionsdb:2CnKp7PAWeup2MzQ@cluster0.fhmjsxn.mongodb.net/?retryWrites=true&w=majority"
    )


settings = Settings()
