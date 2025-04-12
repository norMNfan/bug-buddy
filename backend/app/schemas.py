from pydantic import BaseModel
from typing import List
from datetime import datetime


# TODO: Make non-null once old data is deleted
class Switch(BaseModel):
    id: str
    user_email: str
    name: str | None = None
    content: str | None = None
    interval: int | None = None
    expiration_datetime: datetime | None = None
    is_active: bool | None = None


class Switches(BaseModel):
    switches: List[Switch]

class Repo(BaseModel):
    username: str
    id: str
    full_name: str

class Repos(BaseModel):
    repos: List[Repo]

class Analysis(BaseModel):
    id: str
    log_group: str
