from collections import Counter
from typing import List

from models import TaskData, WarehouseMapping, OutputModel
from db.repository import ExecutionStatisticsRepository
from db import create_session


class WarehouseSelectorService:
    ACCEPTABLE_TIME_OF_EXECUTION = 20
    COEFFICIENTS = [0.1, 0.15, 0.15, 0.2, 0.4]
    WAREHOUSES_RATE = [
        WarehouseMapping.SMALL,
        WarehouseMapping.MEDIUM,
        WarehouseMapping.LARGE,
        WarehouseMapping.XLARGE
    ]

    def __init__(self):
        self._execution_statistics = ExecutionStatisticsRepository(
            session=create_session()
        )

    def _choose_warehouse(self, fraction: float, major_warehouse: WarehouseMapping) -> WarehouseMapping:
        warehouse_index = self.WAREHOUSES_RATE.index(major_warehouse)
        if fraction < 0.5:
            new_warehouse_index = warehouse_index - 1
        elif fraction < 1:
            new_warehouse_index = warehouse_index
        elif fraction < 3:
            new_warehouse_index = warehouse_index + 1
        elif fraction < 10:
            new_warehouse_index = warehouse_index + 2
        else:
            new_warehouse_index = warehouse_index + 3
        new_warehouse_index = min(len(self.WAREHOUSES_RATE), new_warehouse_index)
        new_warehouse_index = max(0, new_warehouse_index)
        return self.WAREHOUSES_RATE[new_warehouse_index]

    def _get_warehouse_type(self, task_data: TaskData) -> WarehouseMapping:
        last_executions = self._execution_statistics.get_last_n_executions(
            task_data.task_name,
            len(self.COEFFICIENTS)
        )
        durations = [statistic.duration for statistic in last_executions]
        average = sum(map(lambda mapping: mapping[0] * mapping[1], zip(durations, self.COEFFICIENTS)))

        fraction = average / self.ACCEPTABLE_TIME_OF_EXECUTION

        major_warehouse_type = Counter(
            [statistic.warehouse_size for statistic in last_executions]
        ).most_common(1)[0][0]
        return self._choose_warehouse(fraction, major_warehouse_type)

    def process_request(self, payload: List[TaskData]) -> List[OutputModel]:
        responses = []
        for task_data in payload:
            warehouse_type = self._get_warehouse_type(task_data)
            responses.append(OutputModel(taskId=task_data.task_id, warehouseSize=warehouse_type))
        return responses
