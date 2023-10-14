from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date

from typing_extensions import Annotated

from app import crud
from app.api import deps
from app.schemas.receivables import ReceivableCreate, ReceivableSummary

router = APIRouter()


@router.post("/receivables", response_model=List[ReceivableCreate], status_code=201)
def create_receivable(
        receivables: List[ReceivableCreate],
        db: Session = Depends(deps.get_db),
):
    """API Endpoint to create a new receivable entry."""
    if len(receivables) == 0:
        return []
    db_receivable = crud.create_receivables(db, receivables)
    return db_receivable


@router.get("/receivables/summary", response_model=ReceivableSummary, status_code=200)
def get_receivable_summary(
        debtor_name: Annotated[str, Query(alias="debtorName")] = None,
        until_date: Annotated[date, Query(alias="untilDate")] = None,
        db: Session = Depends(deps.get_db)
):
    """
    API Endpoint to fetch summary statistics of receivables.
    Allows optional filtering by debtor name and until a certain issue date.
    """
    receivable_summary = crud.get_receivables_summary(db, debtor_name, until_date)
    return receivable_summary
