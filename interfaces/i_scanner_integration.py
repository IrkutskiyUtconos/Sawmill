from abc import ABC, abstractmethod


class IScannerIntegration(ABC):

    @abstractmethod
    def start_scan(self) -> str:
        pass

    @abstractmethod
    def get_scan_result(self, scan_id: str) -> dict:
        pass
