import random
import math
from typing import Dict, Any, Tuple
from .models import EnvState, EnvAction, InventoryState, BacklogState, InTransitState, StepResult

class LogisticsEnv:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.max_weeks = self.config.get("max_weeks", 52)
        self.lead_time = self.config.get("lead_time", 2)
        self.holding_cost = self.config.get("holding_cost", 0.5)
        self.backlog_cost = self.config.get("backlog_cost", 1.0)
        self.unit_price = self.config.get("unit_price", 5.0)
        self.demand_base = self.config.get("demand_base", 15)
        self.demand_amplitude = self.config.get("demand_amplitude", 10)
        self.reset()

    def reset(self) -> EnvState:
        self.inv = [100, 50, 20]
        self.backlog = [0, 0, 0]
        self.to_wh = [0] * self.lead_time
        self.to_retail = [0] * self.lead_time
        self.week = 0
        self.total_reward = 0.0
        self.last_reward = 0.0
        self.done = False
        self.current_demand = self._generate_demand()
        return self.state()

    def state(self) -> EnvState:
        return EnvState(
            inventory=InventoryState(factory=self.inv[0], warehouse=self.inv[1], retail=self.inv[2]),
            backlog=BacklogState(factory=self.backlog[0], warehouse=self.backlog[1], retail=self.backlog[2]),
            in_transit=InTransitState(to_warehouse=list(self.to_wh), to_retail=list(self.to_retail)),
            demand=self.current_demand,
            week=self.week,
            total_reward=self.total_reward,
            last_reward=self.last_reward,
            done=self.done
        )

    def _generate_demand(self) -> int:
        seasonality = math.sin(self.week * (2 * math.PI / 52)) * self.demand_amplitude
        noise = (random.random() - 0.5) * 5
        return max(0, round(self.demand_base + seasonality + noise))

    def step(self, action: EnvAction) -> StepResult:
        if self.done:
            return StepResult(state=self.state(), reward=0.0, done=True, info={"msg": "Env already done"})

        # 1. Receive incoming shipments
        arriving_at_wh = self.to_wh.pop(0) if self.to_wh else 0
        arriving_at_retail = self.to_retail.pop(0) if self.to_retail else 0
        
        self.inv[1] += arriving_at_wh
        self.inv[2] += arriving_at_retail

        # 2. Fulfill demand at Retail
        total_retail_demand = self.current_demand + self.backlog[2]
        fulfilled_retail = min(self.inv[2], total_retail_demand)
        self.inv[2] -= fulfilled_retail
        self.backlog[2] = total_retail_demand - fulfilled_retail

        # 3. Fulfill orders from WH to Retail
        total_wh_order = action.wh_to_retail + self.backlog[1]
        shipped_to_retail = min(self.inv[1], total_wh_order)
        self.inv[1] -= shipped_to_retail
        self.backlog[1] = total_wh_order - shipped_to_retail
        self.to_retail.append(shipped_to_retail)

        # 4. Fulfill orders from Factory to WH
        total_factory_order = action.factory_to_wh + self.backlog[0]
        shipped_to_wh = total_factory_order # Infinite factory capacity
        self.backlog[0] = 0
        self.to_wh.append(shipped_at_wh := shipped_to_wh)

        # 5. Factory Production (Replenish factory stock)
        self.inv[0] = min(200, self.inv[0] + 30)

        # 6. Calculate Reward
        revenue = fulfilled_retail * self.unit_price
        h_cost = sum(i * self.holding_cost for i in self.inv)
        b_cost = sum(b * self.backlog_cost for b in self.backlog)
        reward = revenue - (h_cost + b_cost)

        # 7. Update State
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
            info={
                "revenue": revenue,
                "holding_costs": h_cost,
                "backlog_costs": b_cost
            }
        )
