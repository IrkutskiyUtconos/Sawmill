from abc import ABC, abstractmethod
from typing import List
from domain.cutting_job import CuttingJob


class ICuttingOptimizer(ABC):

    @abstractmethod
    def optimize(self, job: CuttingJob) -> List[List[float]]:
        pass