# reset mock data in database
from sqlalchemy.orm import Session

from app.models.receivables import Receivable


def clear_receivables_data(session: Session):
    """
    Clear all receivables data from the database.
    :param session: The database session object.
    :return: None
    """
    session.query(Receivable).delete()
    session.commit()
