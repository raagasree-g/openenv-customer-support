import json
import os
import random
from typing import Any, Dict, List

from openai import OpenAI

from openenv_logistics.environment import LogisticsEnv
from openenv_logistics.models import EnvAction, EnvState
from openenv_logistics.tasks import TASKS

# Environment variables
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
TASK_NAME = os.getenv("MY_ENV_V4_TASK", "inventory-balancing")
BENCHMARK = os.getenv("MY_ENV_V4_BENCHMARK", "LogisticsFlow-v1")
MAX_STEPS = 52


def get_agent_action(client: OpenAI, state: EnvState) -> EnvAction:
    """
    Simple agent using LLM to decide replenishment quantities.
    In a real scenario, this would be a trained RL agent or a more complex prompt.
    For the baseline, we'll use a prompt that asks the model to decide.
    """
    prompt = f"""
    You are a supply chain manager. Current state:
    - Week: {state.week}
    - Demand: {state.demand}
    - Inventory: Factory={state.inventory.factory}, Warehouse={state.inventory.warehouse}, Retail={state.inventory.retail}
    - Backlog: Factory={state.backlog.factory}, Warehouse={state.backlog.warehouse}, Retail={state.backlog.retail}
    - In-Transit: To Warehouse={state.in_transit.to_warehouse}, To Retail={state.in_transit.to_retail}

    Decide the replenishment quantities for:
    1. Factory to Warehouse (factory_to_wh)
    2. Warehouse to Retail (wh_to_retail)

    Respond in JSON format: {{"factory_to_wh": int, "wh_to_retail": int}}
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a supply chain manager. Respond only with JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        data = json.loads(response.choices[0].message.content)
        return EnvAction(
            factory_to_wh=data.get("factory_to_wh", 20),
            wh_to_retail=data.get("wh_to_retail", 15),
        )
    except Exception as e:
        # Fallback to simple heuristic if LLM fails
        return EnvAction(
            factory_to_wh=max(0, 50 - state.inventory.warehouse),
            wh_to_retail=max(0, 30 - state.inventory.retail),
        )


def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

    # Initialize task and environment
    task_info = TASKS.get(TASK_NAME, TASKS["inventory-balancing"])
    env = LogisticsEnv(config=task_info["config"])
    grader = task_info["grader"]

    state = env.reset()
    history = []
    rewards = []

    print(f"[START] task={TASK_NAME} env={BENCHMARK} model={MODEL_NAME}")

    for step in range(1, MAX_STEPS + 1):
        action = get_agent_action(client, state)
        result = env.step(action)

        state = result.state
        rewards.append(result.reward)
        history.append(
            {
                "step": step,
                "action": action.dict(),
                "reward": result.reward,
                "state": state.dict(),
                "info": result.info,
            }
        )

        print(
            f"[STEP] step={step} action={json.dumps(action.dict())} reward={result.reward:.2f} done={'true' if result.done else 'false'} error=null"
        )

        if result.done:
            break

    # Final scoring
    score = grader.grade(history)
    success = score > 0.5

    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    print(
        f"[END] success={'true' if success else 'false'} steps={len(history)} score={score:.2f} rewards={rewards_str}"
    )


if __name__ == "__main__":
    main()
