from pydantic import BaseModel
from typing import List, Optional

class State(BaseModel):
    customer_query: str
    customer_type: str
    sentiment: str
    issue_type: Optional[str] = None
    history: List[str] = []
    time_elapsed: int = 0

class Action(BaseModel):
    action_type: str
    content: Optional[str] = None

class StepResult(BaseModel):
    observation: dict
    reward: float
    done: bool
    info: dict