# libs import
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
# Local Imports
from db.database import get_session
from models.company_modele import Company

router = APIRouter()


class CompanyCreate(BaseModel):
    name: str
    adress: str


@router.get("/companies")
async def get_companies(session: Session = Depends(get_session)):
    """
     Get all companies

     @param session - SQLAlchemy session to use for database operations

     @return list of founded company(ies)
    """
    companies = session.query(Company).all()
    # Aucun utilisateur trouvés
    if not companies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Aucune entreprise trouvée")
    return companies


@router.get("/companies/{company_id}")
async def get_company(company_id: int, session: Session = Depends(get_session)):
    """
    Get a company by ID

    @param company_id - ID of the company to retrieve
    @param session - SQLAlchemy session to use for database operations

    @return the founded company
    """
    company = session.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Entreprise non trouvée")
    return company


@router.post("/companies")
async def create_company(company: CompanyCreate, session: Session = Depends(get_session)):
    """
    Create a new company

    @param company - CompanyCreate object containing the details of the company to create
    @param session - SQLAlchemy session to use for database operations

    @return the created company
    """
    new_company = Company(
        name=company.name,
        adress=company.adress
    )
    session.add(new_company)
    session.commit()
    session.refresh(new_company)
    return new_company


@router.delete("/companies/{company_id}")
async def delete_company(company_id: int, session: Session = Depends(get_session)):
    """
    Delete a company by ID

    @param company_id - ID of the company to delete
    @param session - SQLAlchemy session to use for database operations

    @return message indicating success or failure
    """
    company = session.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Entreprise non trouvée")

    session.delete(company)
    session.commit()
    return {"message": "Entreprise supprimée avec succès"}


@router.put("/company/{company_id}")
async def update_company(company_id: int, company_data: CompanyCreate, session: Session = Depends(get_session)):
    """
    Update a company by ID

    @param company_id - ID of the company to update
    @param company_data - CompanyCreate object containing the updated details of the company
    @param session - SQLAlchemy session to use for database operations

    @return the updated company
    """
    company = session.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Entreprise non trouvée")

    company.name = company_data.name
    company.adress = company_data.adress
    session.commit()
    session.refresh(company)
    return company
