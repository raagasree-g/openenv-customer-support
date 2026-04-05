import random
import math
import numpy as np

random.seed(42)
np.random.seed(42)

from typing import Dict, Any
from .models import EnvState, EnvAction, InventoryState, BacklogState, InTransitState, StepResult


class LogisticsEnv:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

        self.max_weeks = self.config.get("max_weeks", 52)
        self.lead_time = self.config.get("lead_time", 2)

        # tuned parameters
        self.holding_cost = 0.2
        self.backlog_cost = 0.5
        self.unit_price = 6.0

        # -------------------------
        # ✅ DIFFICULTY SETUP (FIXED)
        # -------------------------
        difficulty = self.config.get("difficulty", "medium")

        if difficulty == "easy":
            self.demand_base = 10
            self.demand_amplitude = 5

        elif difficulty == "medium":
            self.demand_base = 15
            self.demand_amplitude = 8

        else:  # hard
            self.demand_base = 20
            self.demand_amplitude = 12

        self.reset()

    # -------------------------
    # RESET
    # -------------------------
    def reset(self) -> EnvState:
        self.inv = [80, 40, 20]
        self.backlog = [0, 0, 0]

        self.to_wh = [0] * self.lead_time
        self.to_retail = [0] * self.lead_time

        self.week = 0
        self.total_reward = 0.0
        self.last_reward = 0.0
        self.done = False

        self.current_demand = self._generate_demand()
        return self.state()

    # -------------------------
    # STATE
    # -------------------------
    def state(self) -> EnvState:
        return EnvState(
            inventory=InventoryState(
                factory=self.inv[0],
                warehouse=self.inv[1],
                retail=self.inv[2]
            ),
            backlog=BacklogState(
                factory=self.backlog[0],
                warehouse=self.backlog[1],
                retail=self.backlog[2]
            ),
            in_transit=InTransitState(
                to_warehouse=list(self.to_wh),
                to_retail=list(self.to_retail)
            ),
            demand=self.current_demand,
            week=self.week,
            total_reward=self.total_reward,
            last_reward=self.last_reward,
            done=self.done
        )

    # -------------------------
    # DEMAND
    # -------------------------
    def _generate_demand(self) -> int:
        seasonality = math.sin(self.week * (2 * math.pi / 52)) * self.demand_amplitude
        noise = (random.random() - 0.5) * 3
        return max(5, round(self.demand_base + seasonality + noise))

    # -------------------------
    # STEP
    # -------------------------
    def step(self, action: EnvAction) -> StepResult:
        if self.done:
            return StepResult(state=self.state(), reward=0.0, done=True, info={})

        # incoming shipments
        self.inv[1] += self.to_wh.pop(0)
        self.inv[2] += self.to_retail.pop(0)

        # demand fulfillment
        total_demand = self.current_demand + self.backlog[2]
        fulfilled = min(self.inv[2], total_demand)

        self.inv[2] -= fulfilled
        self.backlog[2] = total_demand - fulfilled

        # warehouse to retail
        wh_order = action.wh_to_retail + self.backlog[1]
        shipped_retail = min(self.inv[1], wh_order)

        self.inv[1] -= shipped_retail
        self.backlog[1] = wh_order - shipped_retail
        self.to_retail.append(shipped_retail)

        # factory to warehouse
        factory_order = action.factory_to_wh + self.backlog[0]
        self.backlog[0] = 0
        self.to_wh.append(factory_order)

        # production
        self.inv[0] = min(150, self.inv[0] + 25)

        # -------------------------
        # REWARD (BALANCED)
        # -------------------------
        revenue = fulfilled * self.unit_price
        h_cost = sum(self.inv) * self.holding_cost
        b_cost = sum(self.backlog) * self.backlog_cost

        reward = revenue * 0.6 - (h_cost + b_cost)
        reward += fulfilled * 0.3
        reward -= 0.1 * sum(self.backlog)

        if sum(self.inv) > 250:
            reward -= 1.0

        reward -= 0.05

        # update
        self.week += 1
        self.total_reward += reward
        self.last_reward = reward
        self.current_demand = self._generate_demand()

        if self.week >= self.max_weeks:
            self.done = True

        return StepResult(
            state=self.state(),
            reward=reward,
            done=self.done,
            info={}
        )