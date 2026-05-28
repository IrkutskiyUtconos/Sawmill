import csv
import uuid
import os
from io import StringIO

from domain.cutting_job import CuttingJob
from domain.report import Report
from interfaces.i_report_generator import IReportGenerator


class CsvReportGenerator(IReportGenerator):

    def __init__(self, storage_path: str):
        self._storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)

    def generate(self, job: CuttingJob, stats: dict) -> Report:
        print(f"[CsvReportGenerator] Generating CSV for job {job.id}")

        data = [
            {"field": "job_id", "value": job.id},
            {"field": "created_at", "value": job.created_at.isoformat()},
            {"field": "status", "value": job.status},
            {"field": "material_length", "value": job.material_dimensions[0]},
            {"field": "material_width", "value": job.material_dimensions[1]},
            {"field": "waste_percent", "value": stats.get("waste_percent", 0)},
            {"field": "cutting_time_sec", "value": stats.get("cutting_time_sec", 0)},
        ]

        csv_bytes = self._dict_to_csv(data)

        file_name = f"{job.id}.csv"
        file_path = os.path.join(self._storage_path, file_name)

        with open(file_path, 'wb') as f:
            f.write(csv_bytes)

        report = Report(
            report_id=str(uuid.uuid4()),
            job_id=job.id,
            file_format="csv",
            file_path=file_path,
            size_bytes=len(csv_bytes)
        )

        return report

    def _dict_to_csv(self, data: list) -> bytes:
        if not data:
            return b""

        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

        return output.getvalue().encode('utf-8')