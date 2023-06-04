from pydantic import BaseModel


class Settings(BaseModel):
    date_format = "%d.%m.%Y"


settings = Settings()
