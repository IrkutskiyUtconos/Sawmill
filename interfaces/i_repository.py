from abc import ABC, abstractmethod
from typing import Any, Optional


class IRepository(ABC):
    """Базовый интерфейс репозитория"""

    @abstractmethod
    def save(self, entity: Any) -> bool:
        pass

    @abstractmethod
    def get(self, entity_id: str) -> Optional[Any]:
        pass


class ICuttingRepository(IRepository):
    """Специализированный интерфейс для работы с раскроями"""

    @abstractmethod
    def save_job(self, job) -> bool:
        pass

    @abstractmethod
    def get_job(self, job_id: str):
        pass

    @abstractmethod
    def get_job_stats(self, job_id: str) -> dict:
        pass

    @abstractmethod
    def list_jobs(self, limit: int, offset: int) -> list:
        pass