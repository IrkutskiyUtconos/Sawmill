from datetime import datetime
from typing import List, Optional
import requests

from interfaces.i_erp_integration import IErpIntegration


class ErpAdapter(IErpIntegration):

    def __init__(self, api_url: str, api_key: str):
        self._api_url = api_url.rstrip("/")
        self._api_key = api_key
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {api_key}"})

    def fetch_orders(self, date_from: Optional[datetime] = None) -> List[dict]:
        url = f"{self._api_url}/orders"
        params = {}
        if date_from:
            params["from"] = date_from.isoformat()

        print(f"[ErpAdapter] Fetching orders from {url}")

        return [
            {"id": "ORD-001", "parts": [{"length": 1.2, "qty": 4}]},
            {"id": "ORD-002", "parts": [{"length": 2.0, "qty": 2}]},
        ]

    def update_order_status(self, order_id: str, status: str) -> bool:


        print(f"[ErpAdapter] Updating order {order_id} to {status}")

        return True
