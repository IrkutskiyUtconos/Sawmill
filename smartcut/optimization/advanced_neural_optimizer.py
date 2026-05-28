from typing import List
from optimization.neural_network_optimizer import NeuralNetworkOptimizer
from domain.cutting_job import CuttingJob


class AdvancedNeuralOptimizer(NeuralNetworkOptimizer):

    def __init__(self, model_path: str, heuristic_alpha: float = 0.7):
        super().__init__(model_path)
        self._heuristic_alpha = heuristic_alpha

    def optimize(self, job: CuttingJob) -> List[List[float]]:

        base_plan = super().optimize(job)

        improved_plan = self._apply_heuristics(base_plan)

        print(f"[AdvancedNeuralOptimizer] Applied heuristics (alpha={self._heuristic_alpha})")
        return improved_plan

    def _apply_heuristics(self, plan: List[List[float]]) -> List[List[float]]:
        if not plan:
            return plan

        plan.sort(key=lambda x: x[1] - x[0], reverse=True)

        merged = []
        skip_next = False
        for i in range(len(plan) - 1):
            if skip_next:
                skip_next = False
                continue
            current = plan[i]
            next_seg = plan[i + 1]
            if abs(current[1] - next_seg[0]) < 0.05:
                merged.append([current[0], next_seg[1]])
                skip_next = True
            else:
                merged.append(current)

        if not skip_next and plan:
            merged.append(plan[-1])

        return merged