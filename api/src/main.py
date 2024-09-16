from fastapi import FastAPI
from typing import List

from models import TaskData, OutputModel
from service import WarehouseSelectorService


app = FastAPI()

warehouse_selector = WarehouseSelectorService()


@app.post("/warehouseType")
async def select_warehouse_type(payload: List[TaskData]) -> List[OutputModel]:
    return warehouse_selector.process_request(payload)
