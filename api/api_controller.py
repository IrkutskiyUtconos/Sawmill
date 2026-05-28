from interfaces.i_job_executor import IJobExecutor
from interfaces.i_job_status_provider import IJobStatusProvider
from domain.cutting_job import CuttingJob
import uuid


class ApiController:

    def __init__(self, job_executor: IJobExecutor, status_provider: IJobStatusProvider):
        self._job_executor = job_executor
        self._job_status_provider = status_provider
        self._active_jobs = {}

    def start_cutting(self, job_data: dict) -> str:
        job_id = str(uuid.uuid4())

        job = CuttingJob(
            job_id=job_id,
            material_dimensions=tuple(job_data["material_dimensions"]),
            required_parts=job_data["required_parts"],
            erp_order_id=job_data.get("erp_order_id"),
            scan_data_id=job_data.get("scan_data_id"),
        )

        if not job.validate():
            raise ValueError("Invalid job data")

        self._active_jobs[job_id] = job
        report = self._job_executor.execute(job)

        return job_id

    def get_job_status(self, job_id: str) -> dict:
        status = self._job_status_provider.get_status(job_id)
        return {"job_id": job_id, "status": status}

    def cancel_job(self, job_id: str) -> bool:
        if job_id in self._active_jobs:
            job = self._active_jobs[job_id]
            if job.status in ["new", "optimizing"]:
                job.update_status("failed")
                return True
        return False

    def get_report_url(self, job_id: str) -> str:
        return f"/storage/reports/{job_id}.pdf"
