from datetime import datetime
from typing import Optional


class Report:
    def __init__(
        self, report_id: str, job_id: str, file_format: str, file_path: str, size_bytes: int = 0
    ):
        self.id = report_id
        self.job_id = job_id
        self.generated_at = datetime.now()
        self.format = file_format
        self.file_path = file_path
        self.size_bytes = size_bytes

    def get_content(self) -> Optional[bytes]:
        try:
            with open(self.file_path, "rb") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "job_id": self.job_id,
            "generated_at": self.generated_at.isoformat(),
            "format": self.format,
            "file_path": self.file_path,
            "size_bytes": self.size_bytes,
        }
