from typing import List, Dict, Callable
from datetime import datetime

from interfaces.i_job_executor import IJobExecutor
from interfaces.i_job_status_provider import IJobStatusProvider
from interfaces.i_cutting_optimizer import ICuttingOptimizer
from interfaces.i_machine_integration import IMachineIntegration
from interfaces.i_erp_integration import IErpIntegration
from interfaces.i_scanner_integration import IScannerIntegration
from interfaces.i_repository import ICuttingRepository
from interfaces.i_report_generator import IReportGenerator
from domain.cutting_job import CuttingJob
from domain.report import Report


class SmartCutBackend(IJobExecutor, IJobStatusProvider):
    def __init__(
        self,
        optimizer: ICuttingOptimizer,
        sawmill: IMachineIntegration,
        erp: IErpIntegration,
        scanner: IScannerIntegration,
        repo: ICuttingRepository,
        report_gen: IReportGenerator,
    ):
        self._optimizer = optimizer
        self._sawmill = sawmill
        self._erp = erp
        self._scanner = scanner
        self._repo = repo
        self._report_gen = report_gen

        self._event_handlers: List[Callable] = []
        self._jobs_cache: Dict[str, CuttingJob] = {}

    def execute(self, job: CuttingJob) -> Report:
        """Сквозной процесс выполнения задания"""
        print(f"[SmartCut] Starting job {job.id} at {datetime.now()}")

        job.update_status("optimizing")
        orders = self._erp.fetch_orders()
        print(f"[SmartCut] Fetched {len(orders)} orders from ERP")

        if job.scan_data_id:
            scan_data = self._scanner.get_scan_result(job.scan_data_id)
            print(f"[SmartCut] Using scan data: {scan_data}")

        cutting_plan = self._optimizer.optimize(job)
        job.result_plan = cutting_plan
        print(f"[SmartCut] Optimized cutting plan: {cutting_plan}")

        job.update_status("cutting")
        command = {"job_id": job.id, "plan": cutting_plan}
        success = self._sawmill.send_command(command)

        if not success:
            job.update_status("failed")
            raise RuntimeError("Failed to send command to sawmill")

        machine_status = self._sawmill.get_status()
        print(f"[SmartCut] Machine status: {machine_status}")

        self._repo.save_job(job)
        print("[SmartCut] Saved job to database")

        stats = self._repo.get_job_stats(job.id)
        report = self._report_gen.generate(job, stats)

        if job.erp_order_id:
            self._erp.update_order_status(job.erp_order_id, "completed")

        job.update_status("completed")
        self._notify_complete(job)

        print(f"[SmartCut] Job {job.id} completed successfully")
        return report

    def get_status(self, job_id: str) -> str:
        if job_id in self._jobs_cache:
            return self._jobs_cache[job_id].status

        job = self._repo.get_job(job_id)
        if job:
            return job.status

        return "not_found"

    def on_job_complete(self, callback: Callable):
        self._event_handlers.append(callback)

    def get_job_history(self, filters: dict = None) -> List[CuttingJob]:
        return self._repo.list_jobs(limit=100, offset=0)

    def _notify_complete(self, job: CuttingJob):
        for handler in self._event_handlers:
            handler(job)
