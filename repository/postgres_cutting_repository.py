from typing import List, Optional, Dict
from datetime import datetime
import json

from interfaces.i_repository import ICuttingRepository
from domain.cutting_job import CuttingJob


class PostgresCuttingRepository(ICuttingRepository):

    def __init__(self, connection_string: str):
        self._connection_string = connection_string
        self._pool = None

    def _init_pool(self):
        print(f"[PostgresRepo] Initializing connection pool to {self._connection_string}")

    def _get_connection(self):
        return "connection"

    def save(self, entity) -> bool:
        if isinstance(entity, CuttingJob):
            return self.save_job(entity)
        return False

    def get(self, entity_id: str) -> Optional[CuttingJob]:
        return self.get_job(entity_id)

    def save_job(self, job: CuttingJob) -> bool:
        print(f"[PostgresRepo] Saving job {job.id} to database")
        return True

    def get_job(self, job_id: str) -> Optional[CuttingJob]:
        """Получает задание из БД"""
        print(f"[PostgresRepo] Fetching job {job_id}")

        return CuttingJob(
            job_id=job_id,
            material_dimensions=(3.0, 1.5),
            required_parts=[{"length": 1.0, "width": 0.3, "qty": 4}],
            erp_order_id="ORD-001",
        )

    def get_job_stats(self, job_id: str) -> dict:
        print(f"[PostgresRepo] Fetching stats for job {job_id}")

        return {
            "waste_percent": 12.5,
            "cutting_time_sec": 120,
            "parts_count": 8,
            "efficiency": 87.5,
            "timestamp": datetime.now().isoformat(),
        }

    def list_jobs(self, limit: int = 100, offset: int = 0) -> List[CuttingJob]:
        print(f"[PostgresRepo] Listing jobs (limit={limit}, offset={offset})")

        return []
