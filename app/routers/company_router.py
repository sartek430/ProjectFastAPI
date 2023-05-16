# libs import
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Local Imports
from db.database import get_session
from models.company_modele import Company

router = APIRouter()


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
