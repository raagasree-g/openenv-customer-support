from typing import Dict, Any, List
from .environment import LogisticsEnv
from .models import EnvAction

class TaskGrader:
    def __init__(self, task_name: str):
        self.task_name = task_name

    def grade(self, history: List[Dict[str, Any]]) -> float:
        raise NotImplementedError

class InventoryBalancingGrader(TaskGrader):
    def grade(self, history: List[Dict[str, Any]]) -> float:
        # Easy: Maintain inventory > 0 and backlog < 10
        total_backlog = sum(h["state"]["backlog"]["retail"] for h in history)
        avg_backlog = total_backlog / len(history)
        score = max(0.0, 1.0 - (avg_backlog / 20.0))
        return round(score, 2)

class DemandSurgeGrader(TaskGrader):
    def grade(self, history: List[Dict[str, Any]]) -> float:
        # Medium: Handle high demand with minimal backlog
        # Reward based on total profit / max possible profit
        total_reward = sum(h["reward"] for h in history)
        # Assuming max possible reward is around 100 per week
        score = max(0.0, min(1.0, total_reward / (100.0 * len(history))))
        return round(score, 2)

class GlobalDisruptionGrader(TaskGrader):
    def grade(self, history: List[Dict[str, Any]]) -> float:
        # Hard: Maintain service level during disruption
        # Service level = fulfilled / demand
        fulfilled = sum(h["info"].get("revenue", 0) / 5.0 for h in history)
        demand = sum(h["state"]["demand"] for h in history)
        if demand == 0: return 1.0
        score = min(1.0, fulfilled / demand)
        return round(score, 2)

TASKS = {
    "inventory-balancing": {
        "config": {"demand_base": 10, "demand_amplitude": 5},
        "grader": InventoryBalancingGrader("inventory-balancing")
    },
    "demand-surge": {
        "config": {"demand_base": 25, "demand_amplitude": 15},
        "grader": DemandSurgeGrader("demand-surge")
    },
    "global-disruption": {
        "config": {"lead_time": 4, "demand_base": 20},
        "grader": GlobalDisruptionGrader("global-disruption")
    }
}
