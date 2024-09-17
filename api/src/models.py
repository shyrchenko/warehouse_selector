import datetime
from enum import Enum
from pydantic import BaseModel, Field


class TaskData(BaseModel):
    task_id: str = Field(alias='taskId')
    tenant_name: str = Field(alias='tenantName')
    task_name: str = Field(alias='taskName')
    start_date_time: datetime.datetime = Field(alias='startDatetime')
    number_of_campaigns: int = Field(alias='numberOfCampaigns')
    number_of_customers: int = Field(alias='numberOfCustomers')


class WarehouseMapping(str, Enum):
    SMALL = 'X-Small'
    MEDIUM = 'Medium'
    LARGE = 'Large'
    XLARGE = 'X-Large'


class OutputModel(BaseModel):
    task_id: str = Field(alias='taskId')
    warehouse_size: WarehouseMapping = Field(alias='warehouseSize')
