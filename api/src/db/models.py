from sqlalchemy import Column, String, Integer, Float, DateTime, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ExecutionStatistics(Base):
    __tablename__ = 'execution_statistics'

    tenant_name = Column(String, nullable=True)
    task_id = Column(String, nullable=True)
    start_date_time = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True)
    warehouse_size = Column(String(20), nullable=True)
    number_of_campaigns = Column(Integer, nullable=True)
    number_of_customers = Column(Integer, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint('task_id', 'start_date_time'),
    )
