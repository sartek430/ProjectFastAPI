from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from db.database import get_session
from models.activity_modele import Activity

router = APIRouter()


class ActivityCreate(BaseModel):
    name: str
    description: str


@router.get("/activities")
async def get_activities(session: Session = Depends(get_session)):
    """
    Get all activities

    @param session - SQLAlchemy session to use for database operations

    @return list of found activity(ies)
    """
    activities = session.query(Activity).all()
    if not activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found"
        )
    return activities


@router.get("/activities/{activity_id}")
async def get_activity(activity_id: int, session: Session = Depends(get_session)):
    """
    Get a activity by ID

    @param planning_id - ID of the activity to retrieve
    @param session - SQLAlchemy session to use for database operations

    @return the found activity
    """
    activity = session.query(Activity).get(activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found"
        )
    return activity


@router.post("/activities")
async def create_activity(
    activity_data: ActivityCreate, session: Session = Depends(get_session)
):
    """
    Create a new activity

    @param activity - PlanningCreate object containing the details of the activity to create
    @param session - SQLAlchemy session to use for database operations

    @return the created activity
    """
    new_activity = Activity(
        name=activity_data.name, description=activity_data.description
    )
    session.add(new_activity)
    session.commit()
    session.refresh(new_activity)
    return new_activity


@router.put("/activities/{activity_id}")
async def update_activity(
    activity_id: int,
    activity_data: ActivityCreate,
    session: Session = Depends(get_session),
):
    """
    Delete a activity by ID

    @param planning_id - ID of the activity to delete
    @param session - SQLAlchemy session to use for database operations

    @return message indicating success or failure
    """
    activity = session.query(Activity).get(activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found"
        )

    activity.name = activity_data.name
    activity.description = activity_data.description

    session.commit()
    session.refresh(activity)
    return activity


@router.delete("/activities/{activity_id}")
async def delete_activity(activity_id: int, session: Session = Depends(get_session)):
    """
    Update a activity by ID

    @param planning_id - ID of the activity to update
    @param planning_data - PlanningCreate object containing the updated details of the activity
    @param session - SQLAlchemy session to use for database operations

    @return the updated activity
    """
    activity = session.query(Activity).get(activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found"
        )

    session.delete(activity)
    session.commit()
    return {"message": "Activity deleted successfully"}
