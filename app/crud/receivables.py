from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.receivables import Receivable
from datetime import datetime
from typing import Optional, List

from app.schemas.receivables import ReceivableCreate


def create_receivables(db: Session, receivables: List[ReceivableCreate]) -> List[ReceivableCreate]:
    """
    Create new receivable entry(ies) in the database.

    Params:
    -------
    db : Session
        The database session object.
    receivable : List[dict]
        A list of dictionary containing the receivable data.

    Returns:
    --------
    Receivable
        The created Receivable objects.
    """
    db_receivables = [Receivable(**receivable.model_dump()) for receivable in receivables]
    db.add_all(db_receivables)
    db.commit()
    for db_receivable in db_receivables:
        db.refresh(db_receivable)
    return db_receivables


def get_receivables_summary(db: Session, debtor_name: Optional[str] = None, until_date: Optional[datetime] = None):
    """
    Retrieve summary statistics about receivables from the database.

    Params:
    -------
    db : Session
        The database session object.
    debtor_name : Optional[str]
        (Optional) The name of the debtor to filter the receivables.
    until_date : Optional[datetime]
        (Optional) The end date to filter the receivables summary.

    Returns:
    --------
    dict
        A dictionary containing summary statistics about the receivables.
    """
    # Base query without any filter
    query = db.query(Receivable)

    # Apply filters if provided
    if debtor_name:
        query = query.filter(Receivable.debtor_name == debtor_name)
    if until_date:
        query = query.filter(Receivable.due_date <= until_date)

    # Calculating statistics
    total_open_invoices = query.filter(Receivable.closed_date.is_(None)).count()
    total_closed_invoices = query.filter(Receivable.closed_date.isnot(None)).count()
    total_open_value = query.filter(Receivable.closed_date.is_(None)).with_entities(
        func.sum(Receivable.opening_value)).scalar()
    total_closed_value = query.filter(Receivable.closed_date.isnot(None)).with_entities(
        func.sum(Receivable.paid_value)).scalar()

    # Returning summary in a structured dictionary
    return {
        "total_open_invoices": total_open_invoices,
        "total_closed_invoices": total_closed_invoices,
        "total_open_value": total_open_value or 0,  # Avoiding returning None when there are no entries
        "total_closed_value": total_closed_value or 0  # Avoiding returning None when there are no entries
    }
