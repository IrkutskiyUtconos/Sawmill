from domain.cutting_job import CuttingJob
from domain.report import Report
from interfaces.i_report_generator import IReportGenerator
import uuid
import os


class PdfReportGenerator(IReportGenerator):

    def __init__(self, template_path: str, storage_path: str):
        self._template_path = template_path
        self._storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)

    def generate(self, job: CuttingJob, stats: dict) -> Report:
        print(f"[PdfReportGenerator] Generating PDF for job {job.id}")
        html_content = self._load_template()

        filled_html = self._fill_template(html_content, job, stats)

        pdf_bytes = self._render_pdf(filled_html)

        file_name = f"{job.id}.pdf"
        file_path = os.path.join(self._storage_path, file_name)

        with open(file_path, 'wb') as f:
            f.write(pdf_bytes)

        report = Report(
            report_id=str(uuid.uuid4()),
            job_id=job.id,
            file_format="pdf",
            file_path=file_path,
            size_bytes=len(pdf_bytes)
        )

        return report

    def _load_template(self) -> str:
        return """
        <html>
        <head><title>Cutting Report</title></head>
        <body>
            <h1>Job {job_id}</h1>
            <p>Material: {length} x {width}</p>
            <p>Waste: {waste_percent}%</p>
        </body>
        </html>
        """

    def _fill_template(self, template: str, job: CuttingJob, stats: dict) -> str:
        return template.format(
            job_id=job.id,
            length=job.material_dimensions[0],
            width=job.material_dimensions[1],
            waste_percent=stats.get("waste_percent", 0)
        )

    def _render_pdf(self, html_content: str) -> bytes:
        return b"%PDF-1.4\nPDF_CONTENT_PLACEHOLDER"