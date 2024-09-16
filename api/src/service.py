from typing import List

from models import TaskData, WarehouseMapping, OutputModel


class WarehouseSelectorService:
    @staticmethod
    def _get_warehouse_type(task_data: TaskData) -> WarehouseMapping:
        if task_data.task_name in ['exclude_and_filter_by_higher_today',  'filter_excluded_customers_by_past_and_recs']:
            return WarehouseMapping.MEDIUM
        elif task_data.task_name in ['prepare_customer_campaigns_settings', 'prepare_stream_constraint']:
            return WarehouseMapping.LARGE
        else:
            return WarehouseMapping.SMALL

    def process_request(self, payload: List[TaskData]) -> List[OutputModel]:
        responses = []
        for task_data in payload:
            warehouse_type = self._get_warehouse_type(task_data)
            responses.append(OutputModel(taskId=task_data.task_id, warehouseSize=warehouse_type))
        return responses
