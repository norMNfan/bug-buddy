from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import uuid
from pydantic import BaseModel
from functools import wraps
import asyncio
from datetime import datetime, timezone, timedelta

from ..database import get_db
from ..schemas import Switches, Switch
from ..models import Switch as SwitchModel

router = APIRouter()


class UserEmailRequest(BaseModel):
    user_email: str


class CreateSwitchRequest(BaseModel):
    user_email: str
    name: str
    content: str
    interval: int


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


################
# GET SWITCHES #
################
@router.get("", response_model=Switches)
@log_operation
def get_switches(db: Session = Depends(get_db)):
    db_switches = db.query(SwitchModel).all()

    switches = Switches(
        switches=[
            Switch(
                id=str(switch.id),  # Ensure id is string
                user_email=switch.user_email,
                name=switch.name or "",  # Provide default empty string if None
                content=switch.content or "",  # Provide default empty string if None
                interval=switch.interval,
                expiration_datetime=switch.expiration_datetime,
                is_active=switch.is_active,
            )
            for switch in db_switches
        ]
    )

    return switches


@router.post("/list", response_model=Switches)
@log_operation
def get_switches_v2(request: UserEmailRequest, db: Session = Depends(get_db)):
    db_switches = (
        db.query(SwitchModel).filter(SwitchModel.user_email == request.user_email).all()
    )

    # Convert to Pydantic model
    switches = Switches(
        switches=[
            Switch(
                id=switch.id,
                user_email=switch.user_email,
                name=switch.name,
                content=switch.content,
                interval=switch.interval,
                expiration_datetime=switch.expiration_datetime,
                is_active=switch.is_active,
            )
            for switch in db_switches
        ]
    )

    return switches


@router.get("/{switch_id}", response_model=Switch)
@log_operation
def get_switch_by_id(switch_id: str, db: Session = Depends(get_db)):
    switch = db.query(SwitchModel).filter(SwitchModel.id == switch_id).first()

    if switch is None:
        raise HTTPException(status_code=404, detail="Switch not found")

    return Switch(
        id=switch.id,
        user_email=switch.user_email,
        name=switch.name,
        content=switch.content,
        interval=switch.interval,
        expiration_datetime=switch.expiration_datetime,
        is_active=switch.is_active,
    )


################
# CREATE SWITCH #
################
@router.post("", response_model=Switch)
@log_operation
async def create_switch(request: CreateSwitchRequest, db: Session = Depends(get_db)):
    switch_id = str(uuid.uuid4())

    # Calculate expiration by adding interval days to current time
    current_time = datetime.now(timezone.utc)
    expiration_time = current_time + timedelta(days=request.interval)

    new_switch = SwitchModel(
        id=switch_id,
        user_email=request.user_email,
        name=request.name,
        content=request.content,
        interval=request.interval,
        expiration_datetime=expiration_time,
        is_active=True,
    )

    db.add(new_switch)
    db.commit()
    db.refresh(new_switch)

    return Switch(
        id=new_switch.id,
        user_email=new_switch.user_email,
        name=new_switch.name,
        content=new_switch.content,
        interval=new_switch.interval,
        expiration_datetime=new_switch.expiration_datetime,
        is_active=new_switch.is_active,
    )


################
# UPDATE SWITCH #
################
@router.post("/update/{switch_id}", response_model=Switch)
@log_operation
async def update_switch(
    switch_id: str,
    switch_data: dict = Body(...),
    db: Session = Depends(get_db),
):
    switch = db.query(SwitchModel).filter(SwitchModel.id == switch_id).first()

    if switch is None:
        raise HTTPException(status_code=404, detail="Switch not found")

    switch.name = switch_data.get("name", switch.name)
    switch.content = switch_data.get("content", switch.content)
    switch.interval = switch_data.get("interval", switch.interval)
    switch.expiration_datetime = switch_data.get(
        "expiration_datetime", switch.expiration_datetime
    )
    switch.is_active = switch_data.get("is_active", switch.is_active)
    db.commit()

    return Switch(
        id=switch.id,
        user_email=switch.user_email,
        name=switch.name,
        content=switch.content,
        interval=switch.interval,
        expiration_datetime=switch.expiration_datetime,
        is_active=switch.is_active,
    )


################
# DELETE SWITCH #
################
@router.delete("/{switch_id}", response_model=dict)
@log_operation
async def delete_switch(switch_id: str, db: Session = Depends(get_db)):
    switch = db.query(SwitchModel).filter(SwitchModel.id == switch_id).first()

    if switch is None:
        raise HTTPException(status_code=404, detail="Switch not found")

    db.delete(switch)
    db.commit()

    return {"message": f"Switch {switch_id} deleted successfully"}


################
# CHECKIN SWITCH #
################
@router.post("/checkin/{switch_id}", response_model=Switch)
@log_operation
async def checkin_switch(switch_id: str, db: Session = Depends(get_db)):
    switch = db.query(SwitchModel).filter(SwitchModel.id == switch_id).first()

    if switch is None:
        raise HTTPException(status_code=404, detail="Switch not found")

    # Calculate new expiration by adding interval days to current time
    current_time = datetime.now(timezone.utc)
    new_expiration = current_time + timedelta(days=switch.interval)

    switch.expiration_datetime = new_expiration
    db.commit()

    return Switch(
        id=switch.id,
        user_email=switch.user_email,
        name=switch.name,
        content=switch.content,
        interval=switch.interval,
        expiration_datetime=switch.expiration_datetime,
        is_active=switch.is_active,
    )
