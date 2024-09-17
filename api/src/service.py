from typing import List

from models import TaskData, WarehouseMapping, OutputModel
from db.repository import ExecutionStatisticsRepository
from db import create_session


class WarehouseSelectorService:
    ACCEPTABLE_TIME_OF_EXECUTION = 20
    COEFFICIENTS = [0.1, 0.15, 0.15, 0.2, 0.4]

    def __init__(self):
        self._execution_statistics = ExecutionStatisticsRepository(
            session=create_session()
        )

    def _get_warehouse_type(self, task_data: TaskData) -> WarehouseMapping:
        last_executions = self._execution_statistics.get_last_n_executions(task_data.task_name, 5)
        durations = [statistic.duration for statistic in last_executions]
        average = sum(map(lambda mapping: mapping[0] * mapping[1], zip(durations, self.COEFFICIENTS)))

        fraction = average / self.ACCEPTABLE_TIME_OF_EXECUTION

        if fraction < 1:
            return WarehouseMapping.SMALL
        elif fraction < 3:
            return WarehouseMapping.MEDIUM
        elif fraction < 10:
            return WarehouseMapping.LARGE
        else:
            return WarehouseMapping.XLARGE

    def process_request(self, payload: List[TaskData]) -> List[OutputModel]:
        responses = []
        for task_data in payload:
            warehouse_type = self._get_warehouse_type(task_data)
            responses.append(OutputModel(taskId=task_data.task_id, warehouseSize=warehouse_type))
        return responses
