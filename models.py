from pydantic import BaseModel, AnyHttpUrl
from pydantic.color import Color
from beanie import Document


class Team(Document):
    name: str
    color: Color
    helmet_image: AnyHttpUrl
    ranking: dict[str, int]


class TeamView(BaseModel):
    name: str
    ranking: dict
