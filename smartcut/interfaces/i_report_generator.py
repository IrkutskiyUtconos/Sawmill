from abc import ABC, abstractmethod
from domain.cutting_job import CuttingJob
from domain.report import Report


class IReportGenerator(ABC):
    @abstractmethod
    def generate(self, job: CuttingJob, stats: dict) -> Report:
        pass