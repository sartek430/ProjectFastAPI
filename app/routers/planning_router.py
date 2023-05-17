# libs import
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
# system import
from datetime import date, datetime
# Local Imports
from db.database import get_session
from models.planning_modele import Planning

router = APIRouter()


class PlanningCreate(BaseModel):
    day: date
    start_time: str
    end_time: str


@router.get("/plannings")
async def get_plannings(session: Session = Depends(get_session)):
    """
    Get all plannings

    @param session - SQLAlchemy session to use for database operations

    @return list of found planning(s)
    """
    plannings = session.query(Planning).all()
    if not plannings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No planning found")
    return plannings


@router.get("/plannings/{planning_id}")
async def get_planning(planning_id: int, session: Session = Depends(get_session)):
    """
    Get a planning by ID

    @param planning_id - ID of the planning to retrieve
    @param session - SQLAlchemy session to use for database operations

    @return the found planning
    """
    planning = session.query(Planning).filter(
        Planning.id == planning_id).first()
    if not planning:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")
    return planning


@router.post("/plannings")
async def create_planning(planning: PlanningCreate, session: Session = Depends(get_session)):
    """
    Create a new planning

    @param planning - PlanningCreate object containing the details of the planning to create
    @param session - SQLAlchemy session to use for database operations

    @return the created planning
    """
    planning.start_time = datetime.strptime(
        planning.start_time, "%H:%M:%S").time()
    planning.end_time = datetime.strptime(planning.end_time, "%H:%M:%S").time()
    new_planning = Planning(
        day=planning.day,
        start_time=planning.start_time,
        end_time=planning.end_time
    )
    session.add(new_planning)
    session.commit()
    session.refresh(new_planning)
    return new_planning


@router.delete("/plannings/{planning_id}")
async def delete_planning(planning_id: int, session: Session = Depends(get_session)):
    """
    Delete a planning by ID

    @param planning_id - ID of the planning to delete
    @param session - SQLAlchemy session to use for database operations

    @return message indicating success or failure
    """
    planning = session.query(Planning).filter(
        Planning.id == planning_id).first()
    if not planning:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")

    session.delete(planning)
    session.commit()
    return {"message": "Planning deleted successfully"}


@router.put("/plannings/{planning_id}")
async def update_planning(planning_id: int, planning_data: PlanningCreate, session: Session = Depends(get_session)):
    """
    Update a planning by ID

    @param planning_id - ID of the planning to update
    @param planning_data - PlanningCreate object containing the updated details of the planning
    @param session - SQLAlchemy session to use for database operations

    @return the updated planning
    """
    planning_data.start_time = datetime.strptime(
        planning_data.start_time, "%H:%M:%S").time()
    planning_data.end_time = datetime.strptime(
        planning_data.end_time, "%H:%M:%S").time()

    planning = session.query(Planning).filter(
        Planning.id == planning_id).first()
    if not planning:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")

    planning.day = planning_data.day
    planning.start_time = planning_data.start_time
    planning.end_time = planning_data.end_time

    session.commit()
    session.refresh(planning)
    return planning_data
