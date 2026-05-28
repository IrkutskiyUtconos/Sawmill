from interfaces.i_machine_integration import IMachineIntegration


class SawmillIntegration(IMachineIntegration):
    def __init__(self, ip: str, port: int, timeout: float = 5.0):
        self._ip = ip
        self._port = port
        self._timeout = timeout
        self._connected = False

    def _connect(self) -> bool:
        print(f"[SawmillIntegration] Connecting to {self._ip}:{self._port}")
        self._connected = True
        return True

    def send_command(self, command: dict) -> bool:
        if not self._connected:
            self._connect()

        print(f"[SawmillIntegration] Sending command: {command}")
        return True

    def get_status(self) -> dict:
        return {
            "online": self._connected,
            "busy": False,
            "error": None,
            "progress": 100,
            "temperature": 45.2,
        }
