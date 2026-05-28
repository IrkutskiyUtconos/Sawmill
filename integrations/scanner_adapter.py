from interfaces.i_scanner_integration import IScannerIntegration
import uuid


class ScannerAdapter(IScannerIntegration):
    def __init__(self, serial_port: str, baud_rate: int = 115200):
        self._serial_port = serial_port
        self._baud_rate = baud_rate
        self._active_scans = {}

    def _connect_serial(self):
        print(f"[ScannerAdapter] Connecting to {self._serial_port} at {self._baud_rate}")

    def start_scan(self) -> str:
        scan_id = str(uuid.uuid4())
        self._active_scans[scan_id] = "scanning"
        print(f"[ScannerAdapter] Started scan {scan_id}")
        return scan_id

    def get_scan_result(self, scan_id: str) -> dict:
        if scan_id not in self._active_scans:
            return None

        return {
            "scan_id": scan_id,
            "length": 3.0,
            "width": 1.5,
            "thickness": 0.05,
            "defects": [[0.5, 0.2], [1.3, 0.7]],
            "quality_score": 0.95
        }