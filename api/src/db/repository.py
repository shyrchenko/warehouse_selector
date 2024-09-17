from sqlalchemy.orm import Session
from sqlalchemy import desc
from .models import ExecutionStatistics


class ExecutionStatisticsRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_last_n_executions(self, task_id: str, n: int):
        return self.session.query(
            ExecutionStatistics
        ).filter_by(
            task_id=task_id
        ).order_by(
            desc(ExecutionStatistics.start_date_time)
        ).limit(n).all()
