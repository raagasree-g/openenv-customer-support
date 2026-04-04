from pydantic import BaseModel
from typing import List, Dict, Optional

class InventoryState(BaseModel):
    factory: int
    warehouse: int
    retail: int

class BacklogState(BaseModel):
    factory: int
    warehouse: int
    retail: int

class InTransitState(BaseModel):
    to_warehouse: List[int]
    to_retail: List[int]

class EnvState(BaseModel):
    inventory: InventoryState
    backlog: BacklogState
    in_transit: InTransitState
    demand: int
    week: int
    total_reward: float
    last_reward: float
    done: bool

class EnvAction(BaseModel):
    factory_to_wh: int
    wh_to_retail: int

class StepResult(BaseModel):
    state: EnvState
    reward: float
    done: bool
    info: Dict
