import pytest
from unittest.mock import Mock, patch
from domain.cutting_job import CuttingJob
from domain.report import Report
from api.api_controller import ApiController
from core.smart_cut_backend import SmartCutBackend


class TestCuttingJob:

    def test_create_job(self):
        job = CuttingJob(
            job_id="test-1",
            material_dimensions=(3.0, 1.5),
            required_parts=[{"length": 1.2, "width": 0.3, "qty": 4}],
        )
        assert job.id == "test-1"
        assert job.status == "new"
        assert job.material_dimensions == (3.0, 1.5)

    def test_validate_correct_job(self):
        job = CuttingJob(
            job_id="test-1",
            material_dimensions=(3.0, 1.5),
            required_parts=[{"length": 1.2, "width": 0.3, "qty": 4}],
        )
        assert job.validate() is True

    def test_validate_invalid_dimensions(self):
        job = CuttingJob(
            job_id="test-1",
            material_dimensions=(0, -1.5),
            required_parts=[{"length": 1.2, "width": 0.3, "qty": 4}],
        )
        assert job.validate() is False

    def test_update_status(self):
        job = CuttingJob("test-1", (3.0, 1.5), [])
        job.update_status("optimizing")
        assert job.status == "optimizing"

        job.update_status("completed")
        assert job.status == "completed"

    def test_to_dict(self):
        job = CuttingJob("test-1", (3.0, 1.5), [{"length": 1.2, "qty": 2}])
        result = job.to_dict()
        assert result["id"] == "test-1"
        assert result["status"] == "new"
        assert "created_at" in result


class TestReport:

    def test_create_report(self):
        report = Report(
            report_id="rep-1",
            job_id="job-1",
            file_format="pdf",
            file_path="/tmp/report.pdf",
            size_bytes=1024,
        )
        assert report.id == "rep-1"
        assert report.job_id == "job-1"
        assert report.format == "pdf"

    def test_to_dict(self):
        report = Report("rep-1", "job-1", "pdf", "/tmp/report.pdf")
        result = report.to_dict()
        assert result["id"] == "rep-1"
        assert result["format"] == "pdf"


class TestApiController:
    @pytest.fixture
    def mock_backend(self):
        backend = Mock()
        backend.execute.return_value = Report("rep-1", "job-1", "pdf", "/tmp/report.pdf")
        backend.get_status.return_value = "completed"
        return backend

    def test_start_cutting(self, mock_backend):
        controller = ApiController(mock_backend, mock_backend)

        job_data = {
            "material_dimensions": [3.0, 1.5],
            "required_parts": [{"length": 1.2, "width": 0.3, "qty": 4}],
        }

        job_id = controller.start_cutting(job_data)
        assert job_id is not None
        assert mock_backend.execute.called

    def test_get_job_status(self, mock_backend):
        controller = ApiController(mock_backend, mock_backend)

        status = controller.get_job_status("job-123")
        assert status["status"] == "completed"
        assert status["job_id"] == "job-123"


class TestSmartCutBackend:

    @pytest.fixture
    def mock_dependencies(self):
        return {
            "optimizer": Mock(),
            "sawmill": Mock(),
            "erp": Mock(),
            "scanner": Mock(),
            "repo": Mock(),
            "report_gen": Mock(),
        }

    def test_execute_job_success(self, mock_dependencies):
        mock_dependencies["optimizer"].optimize.return_value = [[0, 1.2], [1.2, 2.4]]
        mock_dependencies["sawmill"].send_command.return_value = True
        mock_dependencies["sawmill"].get_status.return_value = {"online": True}
        mock_dependencies["erp"].fetch_orders.return_value = [{"id": "ORD-1"}]
        mock_dependencies["repo"].get_job_stats.return_value = {"waste_percent": 10.5}
        mock_dependencies["report_gen"].generate.return_value = Report(
            "rep-1", "job-1", "pdf", "/tmp/report.pdf"
        )

        backend = SmartCutBackend(**mock_dependencies)

        job = CuttingJob("job-1", (3.0, 1.5), [{"length": 1.2, "qty": 2}])
        report = backend.execute(job)

        assert report is not None
        mock_dependencies["optimizer"].optimize.assert_called_once()
        mock_dependencies["sawmill"].send_command.assert_called_once()
        mock_dependencies["repo"].save_job.assert_called_once()

    def test_execute_job_fail_on_sawmill(self, mock_dependencies):
        mock_dependencies["sawmill"].send_command.return_value = False
        mock_dependencies["optimizer"].optimize.return_value = [[0, 1.2]]

        backend = SmartCutBackend(**mock_dependencies)

        job = CuttingJob("job-1", (3.0, 1.5), [])

        with pytest.raises(RuntimeError, match="Failed to send command"):
            backend.execute(job)

    def test_get_status_from_cache(self, mock_dependencies):
        backend = SmartCutBackend(**mock_dependencies)
        job = CuttingJob("job-1", (3.0, 1.5), [])
        job.update_status("completed")

        backend._jobs_cache["job-1"] = job

        status = backend.get_status("job-1")
        assert status == "completed"

    def test_get_status_from_repo(self, mock_dependencies):
        job = CuttingJob("job-1", (3.0, 1.5), [])
        job.update_status("optimizing")
        mock_dependencies["repo"].get_job.return_value = job

        backend = SmartCutBackend(**mock_dependencies)
        status = backend.get_status("job-1")

        assert status == "optimizing"
        mock_dependencies["repo"].get_job.assert_called_with("job-1")


class TestOptimizers:

    def test_neural_optimizer(self):
        from optimization.neural_network_optimizer import NeuralNetworkOptimizer

        optimizer = NeuralNetworkOptimizer("test_model.onnx")
        job = CuttingJob("job-1", (3.0, 1.5), [{"length": 1.2, "qty": 2}])

        plan = optimizer.optimize(job)

        assert isinstance(plan, list)
        assert len(plan) > 0

    def test_advanced_optimizer_inheritance(self):
        from optimization.neural_network_optimizer import NeuralNetworkOptimizer
        from optimization.advanced_neural_optimizer import AdvancedNeuralOptimizer

        assert issubclass(AdvancedNeuralOptimizer, NeuralNetworkOptimizer)

    def test_advanced_optimizer_with_heuristics(self):
        from optimization.advanced_neural_optimizer import AdvancedNeuralOptimizer

        optimizer = AdvancedNeuralOptimizer("test_model.onnx", heuristic_alpha=0.8)
        job = CuttingJob("job-1", (3.0, 1.5), [{"length": 1.2, "qty": 2}])

        plan = optimizer.optimize(job)

        assert isinstance(plan, list)


class TestIntegrations:

    def test_sawmill_integration(self):
        from integrations.sawmill_integration import SawmillIntegration

        sawmill = SawmillIntegration("127.0.0.1", 502)
        result = sawmill.send_command({"test": "command"})
        status = sawmill.get_status()

        assert result is True
        assert "online" in status

    def test_erp_adapter(self):
        from integrations.erp_adapter import ErpAdapter

        erp = ErpAdapter("https://api.test.com", "test-key")

        orders = erp.fetch_orders()
        assert isinstance(orders, list)

        result = erp.update_order_status("ORD-123", "completed")
        assert result is True

    def test_scanner_adapter(self):
        from integrations.scanner_adapter import ScannerAdapter

        scanner = ScannerAdapter("COM3", 9600)

        scan_id = scanner.start_scan()
        assert scan_id is not None

        result = scanner.get_scan_result(scan_id)
        assert result is not None
        assert "scan_id" in result


class TestRepository:

    def test_postgres_repository_save_job(self):
        from repository.postgres_cutting_repository import PostgresCuttingRepository

        repo = PostgresCuttingRepository("postgresql://test:test@localhost/test")
        job = CuttingJob("job-1", (3.0, 1.5), [])

        result = repo.save_job(job)
        assert result is True

    def test_postgres_repository_get_job_stats(self):
        from repository.postgres_cutting_repository import PostgresCuttingRepository

        repo = PostgresCuttingRepository("postgresql://test:test@localhost/test")

        stats = repo.get_job_stats("job-1")

        assert "waste_percent" in stats
        assert "cutting_time_sec" in stats


class TestReportGenerators:

    def test_pdf_report_generator(self, tmp_path):
        from reports.pdf_report_generator import PdfReportGenerator

        storage_path = str(tmp_path / "reports")
        generator = PdfReportGenerator("template.html", storage_path)

        job = CuttingJob("job-1", (3.0, 1.5), [])
        stats = {"waste_percent": 15.5}

        report = generator.generate(job, stats)

        assert report.format == "pdf"
        assert report.job_id == "job-1"

    def test_csv_report_generator(self, tmp_path):
        from reports.csv_report_generator import CsvReportGenerator

        storage_path = str(tmp_path / "reports")
        generator = CsvReportGenerator(storage_path)

        job = CuttingJob("job-1", (3.0, 1.5), [])
        stats = {"waste_percent": 15.5}

        report = generator.generate(job, stats)

        assert report.format == "csv"
        assert report.job_id == "job-1"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
