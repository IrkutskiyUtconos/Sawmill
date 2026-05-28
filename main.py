from api.api_controller import ApiController
from core.smart_cut_backend import SmartCutBackend
from optimization.neural_network_optimizer import NeuralNetworkOptimizer
from integrations.sawmill_integration import SawmillIntegration
from integrations.erp_adapter import ErpAdapter
from integrations.scanner_adapter import ScannerAdapter
from repository.postgres_cutting_repository import PostgresCuttingRepository
from reports.pdf_report_generator import PdfReportGenerator


def main():
    print("=" * 60)
    print("SmartCut System Starting...")
    print("=" * 60)

    repo = PostgresCuttingRepository("postgresql://localhost:5432/smartcut")

    optimizer = NeuralNetworkOptimizer("models/cutting_v3.onnx")
    sawmill = SawmillIntegration("192.168.1.100", 502)
    erp = ErpAdapter("https://erp.company.com/api", "secret-api-key")
    scanner = ScannerAdapter("COM3", 115200)

    report_gen = PdfReportGenerator("templates/report.html", "/var/storage/reports")

    backend = SmartCutBackend(
        optimizer=optimizer,
        sawmill=sawmill,
        erp=erp,
        scanner=scanner,
        repo=repo,
        report_gen=report_gen
    )

    api = ApiController(
        job_executor=backend,
        status_provider=backend
    )

    print("\n[Demo] Creating new cutting job...")

    job_data = {
        "material_dimensions": [3.0, 1.5],
        "required_parts": [
            {"length": 1.2, "width": 0.3, "qty": 4},
            {"length": 0.8, "width": 0.3, "qty": 2},
        ],
        "erp_order_id": "ORD-12345",
        "scan_data_id": "SCAN-67890"
    }

    try:
        job_id = api.start_cutting(job_data)
        print(f"\n[Demo] Job started with ID: {job_id}")

        status = api.get_job_status(job_id)
        print(f"[Demo] Job status: {status}")

        report_url = api.get_report_url(job_id)
        print(f"[Demo] Report URL: {report_url}")

    except Exception as e:
        print(f"[Demo] Error: {e}")

    print("\n" + "=" * 60)
    print("SmartCut System Ready")
    print("=" * 60)


if __name__ == "__main__":
    main()