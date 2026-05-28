from abc import ABC, abstractmethod


class IMachineIntegration(ABC):

    @abstractmethod
    def send_command(self, command: dict) -> bool:
        pass

    @abstractmethod
    def get_status(self) -> dict:
        pass
