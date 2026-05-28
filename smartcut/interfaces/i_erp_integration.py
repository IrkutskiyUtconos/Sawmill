from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional


class IErpIntegration(ABC):

    @abstractmethod
    def fetch_orders(self, date_from: Optional[datetime] = None) -> List[dict]:
        pass

    @abstractmethod
    def update_order_status(self, order_id: str, status: str) -> bool:
        pass