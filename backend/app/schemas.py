from pydantic import BaseModel
from typing import Any, List
from portia import Plan


class Repo(BaseModel):
    username: str
    id: str
    full_name: str

class Repos(BaseModel):
    repos: List[Repo]

class Analysis(BaseModel):
    id: str
    log_group: str
    plan_id: str
    query_steps: List[Any]
    plan: Plan
