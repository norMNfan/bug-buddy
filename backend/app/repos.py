import time
import requests
import os
import re
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from functools import wraps
import asyncio

from .database import get_db
from .schemas import ContinuePlanResponse, CreatePlanResponse, RunPlanResponse, PlanStatusResponse, Repo, Repos
from .models import Repo as RepoModel

from .portia_impl import create_plan, run_plan, resume_run

router = APIRouter()


class UserEmailRequest(BaseModel):
    user_email: str


class AddRepoRequest(BaseModel):
    username: str
    id: str
    full_name: str


class AddReposRequest(BaseModel):
    repos: List[AddRepoRequest]


class CreatePlanRequest(BaseModel):
    repo_id: str
    full_name: str


class RunPlanRequest(BaseModel):
    plan_id: str

class ContinuePlanRequest(BaseModel):
    plan_run_id: str
    option: str



def log_operation(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"Entering {func.__name__}")
        result = (
            await func(*args, **kwargs)
            if asyncio.iscoroutinefunction(func)
            else func(*args, **kwargs)
        )
        # Convert result to string safely, handling potential circular references
        result_str = str(result) if result else "None"
        print(f"Exiting {func.__name__} with result: {result_str}")
        return result

    return wrapper


###########
# ANALYZE #
###########
# TODO - Implement AI Agent
@router.post("/createplan", response_model=CreatePlanResponse)
@log_operation
async def createplan(request: CreatePlanRequest):
    plan = create_plan()
    print(plan)

    match = re.search(r"UUID\('([a-f0-9\-]{36})'\)", str(plan))
    plan_id = "plan-" + match.group(1)
    
    response = CreatePlanResponse(
        plan_id=plan_id
    )

    return response


@router.post("/runplan", response_model=RunPlanResponse)
@log_operation
async def runplan(request: RunPlanRequest):
    plan_id = request.plan_id

    plan_result = run_plan(plan_id)
    print(f"plan_result: {plan_result}")

    plan_run_id = re.search(r"plan_run_id=PlanRunUUID\(uuid=UUID\('([0-9a-f-]+)'\)\)", str(plan_result)).group(1)

    response = RunPlanResponse(
        plan_run_id=plan_run_id,
        user_guidance=plan_result.user_guidance,
        options=plan_result.options
    )

    return response


@router.post("/continueplan", response_model=ContinuePlanResponse)
@log_operation
async def continueplan(request: ContinuePlanRequest):
    res = resume_run(request.plan_run_id, request.option)

    response = ContinuePlanResponse(
        output=str(res)
    )

    return response


@router.get("/getplanstatus/{plan_id}", response_model=PlanStatusResponse)
@log_operation
def get_plan_status(plan_id: str):
    
    try:
        # Use environment variable or securely stored key
        api_key = os.getenv("PORTIA_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="Portia API key not configured")

        portia_url = f"https://api.portialabs.ai/api/v0/plans/{plan_id}"

        headers = {
            "Authorization": f"Api-Key {api_key}",
            "Accept": "application/json",
        }

        time.sleep(10)
        response = requests.get(portia_url, headers=headers)
        print(f"Porta get plan status response: {response['steps']}")

        res = PlanStatusResponse(output=str(response['steps']))

        return res

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#########
# REPOS #
#########
@router.get("", response_model=Repos)
@log_operation
def get_repos(db: Session = Depends(get_db)):
    """
    Retrieve all repositories from the database.
    """
    repos = db.query(RepoModel).all()

    response = Repos(
        repos = [
            Repo(
                id = repo.id,
                username = repo.username,
                full_name = repo.full_name,
            )
            for repo in repos
        ]
    )

    print(len(repos))

    return response


@router.post("", response_model=dict)
@log_operation
async def add_repos(request: AddReposRequest, db: Session = Depends(get_db)):
    for repo in request.repos:
        # Try to find existing repo by ID
        existing_repo = db.query(RepoModel).filter_by(id=repo.id).first()

        if existing_repo:
            # Update existing repo
            existing_repo.username = repo.username
            existing_repo.full_name = repo.full_name
            print(f"Updated repo: {repo.id}")
        else:
            # Insert new repo
            new_repo = RepoModel(
                id=repo.id,
                username=repo.username,
                full_name=repo.full_name
            )
            db.add(new_repo)
            print(f"Added new repo: {repo.id}")

    db.commit()

    return {"message": "Repos upserted successfully"}
