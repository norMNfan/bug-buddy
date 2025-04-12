from pydantic import BaseModel
from typing import Any, List
from portia import Plan


class Repo(BaseModel):
    username: str
    id: str
    full_name: str

class Repos(BaseModel):
    repos: List[Repo]

class CreatePlanResponse(BaseModel):
    plan_id: str
    

class RunPlanResponse(BaseModel):
    plan_run_id: str
    user_guidance: str
    options: List[str]

class PlanStatusResponse(BaseModel):
    output: str
