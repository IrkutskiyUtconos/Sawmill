from datetime import datetime
from typing import List, Dict, Tuple, Optional


class CuttingJob:

    def __init__(
        self,
        job_id: str,
        material_dimensions: Tuple[float, float],
        required_parts: List[Dict[str, float]],
        erp_order_id: Optional[str] = None,
        scan_data_id: Optional[str] = None,
    ):
        self.id = job_id
        self.created_at = datetime.now()
        self.status = "new"
        self.material_dimensions = material_dimensions
        self.required_parts = required_parts
        self.erp_order_id = erp_order_id
        self.scan_data_id = scan_data_id
        self.result_plan = None

    def validate(self) -> bool:
        if self.material_dimensions[0] <= 0 or self.material_dimensions[1] <= 0:
            return False
        for part in self.required_parts:
            if part.get("length", 0) <= 0 or part.get("width", 0) <= 0:
                return False
            if part.get("qty", 0) <= 0:
                return False
        return True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "material_dimensions": self.material_dimensions,
            "required_parts": self.required_parts,
            "erp_order_id": self.erp_order_id,
            "scan_data_id": self.scan_data_id,
        }

    def update_status(self, new_status: str):
        valid_statuses = ["new", "optimizing", "cutting", "completed", "failed"]
        if new_status in valid_statuses:
            self.status = new_status
