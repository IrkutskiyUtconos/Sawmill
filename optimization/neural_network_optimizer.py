from typing import List, Dict
import json
from interfaces.i_cutting_optimizer import ICuttingOptimizer
from domain.cutting_job import CuttingJob


class NeuralNetworkOptimizer(ICuttingOptimizer):

    def __init__(self, model_path: str):
        self._model_path = model_path
        self._cache: Dict[str, List[List[float]]] = {}
        self._model = None

    def _load_model(self):
        print(f"[NeuralNetworkOptimizer] Loading model from {self._model_path}")
        self._model = "pretrained_model"  # заглушка

    def optimize(self, job: CuttingJob) -> List[List[float]]:

        cache_key = f"{job.material_dimensions}_{json.dumps(job.required_parts)}"
        if cache_key in self._cache:
            print(f"[NeuralNetworkOptimizer] Returning cached result")
            return self._cache[cache_key]

        if self._model is None:
            self._load_model()

        length, width = job.material_dimensions
        total_needed = sum(part["length"] * part["qty"] for part in job.required_parts)

        cutting_plan = []
        current_pos = 0.0
        for part in job.required_parts:
            for _ in range(int(part["qty"])):
                cutting_plan.append([current_pos, current_pos + part["length"]])
                current_pos += part["length"]

        self._cache[cache_key] = cutting_plan
        return cutting_plan
