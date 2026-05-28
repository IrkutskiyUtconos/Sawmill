from abc import ABC, abstractmethod
from domain.cutting_job import CuttingJob
from domain.report import Report


class IJobExecutor(ABC):

    @abstractmethod
    def execute(self, job: CuttingJob) -> Report:
        pass