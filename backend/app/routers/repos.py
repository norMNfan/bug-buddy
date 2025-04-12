from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from functools import wraps
import asyncio

from ..database import get_db
from ..schemas import Analysis, Repo, Repos
from ..models import Repo as RepoModel

router = APIRouter()


class UserEmailRequest(BaseModel):
    user_email: str


class CreateSwitchRequest(BaseModel):
    user_email: str
    name: str
    content: str
    interval: int


class AddRepoRequest(BaseModel):
    username: str
    id: str
    full_name: str


class AddReposRequest(BaseModel):
    repos: List[AddRepoRequest]


class AnalyzeRepoRequest(BaseModel):
    repo_id: str
    full_name: str



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
@router.post("/analyze", response_model=Analysis)
@log_operation
async def analyze(request: AnalyzeRepoRequest, db: Session = Depends(get_db)):
    repo_name_to_log_group_map = {
        "norMNfan/hello-aws": "/aws/lambda/sam-app-HelloWorldFunction-4ifWr8G1aiJP"
    }

    log_group = repo_name_to_log_group_map[request.full_name]
    
    response = Analysis(id='1234', log_group=log_group)

    return response


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
