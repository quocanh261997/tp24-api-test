from sqlalchemy import Column, Integer, String, Float, Date, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Receivable(Base):
    __tablename__ = 'receivables'

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String)
    currency_code = Column(String)
    issue_date = Column(Date, index=True)  # Single-column index
    opening_value = Column(Float)
    paid_value = Column(Float)
    due_date = Column(Date)
    closed_date = Column(Date)
    cancelled = Column(Boolean)
    debtor_name = Column(String, index=True)  # Single-column index
    debtor_reference = Column(String)
    debtor_address1 = Column(String)
    debtor_address2 = Column(String)
    debtor_town = Column(String)
    debtor_state = Column(String)
    debtor_zip = Column(String)
    debtor_country_code = Column(String)
    debtor_registration_number = Column(String)

    # Multiple column index
    __table_args__ = (
        Index('idx_name_issue', 'debtor_name', 'issue_date'),
    )
