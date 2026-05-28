from abc import ABC, abstractmethod


class IJobStatusProvider(ABC):

    @abstractmethod
    def get_status(self, job_id: str) -> str:
        pass
