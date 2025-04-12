from pydantic import BaseModel
from typing import List


class Repo(BaseModel):
    username: str
    id: str
    full_name: str

class Repos(BaseModel):
    repos: List[Repo]

class Analysis(BaseModel):
    id: str
    log_group: str
