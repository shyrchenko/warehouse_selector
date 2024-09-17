import requests
import json


def test_endpoint(api_host: str, static_data_path: str):
    endpoint = 'warehouseType'

    with open(static_data_path, 'r') as f:
        payload = json.load(f)

    response = requests.post(api_host + endpoint, json=payload)
    assert response.json() == [
      {
        "taskId": "0",
        "warehouseSize": "X-Small"
      },
      {
        "taskId": "1",
        "warehouseSize": "Large"
      },
      {
        "taskId": "2",
        "warehouseSize": "Medium"
      }
    ]
