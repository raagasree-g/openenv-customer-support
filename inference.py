import os
from openenv_logistics.environment import LogisticsEnv
from openenv_logistics.models import EnvAction

MODEL_NAME = "baseline-agent"
TASKS = ["easy", "medium", "hard"]
MAX_STEPS = 20


last_demand = None
def get_agent_action(state):
    inv = state["inventory"]
    backlog = state["backlog"]
    demand = state["demand"]

    warehouse = inv["warehouse"]
    retail = inv["retail"]
    factory = inv["factory"]

    # -------------------------
    # BALANCED TARGETS
    # -------------------------
    target_retail = demand + 3
    target_wh = demand * 1.4

    wh_to_retail = 0
    factory_to_wh = 0

    # -------------------------
    # RETAIL SUPPLY (adaptive)
    # -------------------------
    if retail < target_retail:
        deficit = target_retail - retail
        wh_to_retail = min(deficit, warehouse, 18)

    # -------------------------
    # WAREHOUSE REFILL (moderate)
    # -------------------------
    if warehouse < target_wh:
        deficit = target_wh - warehouse
        factory_to_wh = min(deficit, 25)

    # -------------------------
    # BACKLOG HANDLING (priority)
    # -------------------------
    if backlog["retail"] > 0:
        wh_to_retail = min(20, warehouse)

    if backlog["warehouse"] > 0:
        factory_to_wh = min(30, factory)

    return EnvAction(
        factory_to_wh=int(factory_to_wh),
        wh_to_retail=int(wh_to_retail)
    )

def run_episode(env, task):
    state = env.reset().model_dump()
    done = False
    step = 0
    rewards = []

    print(f"[START] task={task} env=openenv-logistics model={MODEL_NAME}")

    while not done and step < MAX_STEPS:
        step += 1
        action = get_agent_action(state)

        result = env.step(action)
        state = result.state.model_dump()

        reward = float(result.reward)
        done = result.done

        rewards.append(f"{reward:.2f}")

        print(f"[STEP] step={step} action={action.model_dump()} reward={reward:.2f} done={'true' if done else 'false'} error=null")

    backlog_total = sum(state["backlog"].values())
    inventory_total = sum(state["inventory"].values())

    inventory_total = sum(state["inventory"].values())
    backlog_total = sum(state["backlog"].values())

    score = max(0.0, min(1.0,
    0.7 * (1 - backlog_total / 150) +
    0.3 * (inventory_total / 200)
))

    success = score > 0.35


    print(f"[END] success={'true' if success else 'false'} steps={step} score={score:.2f} rewards={','.join(rewards)}")


def main():
    tasks = ["easy", "medium", "hard"]

    for task in tasks:
        env = LogisticsEnv(config={"difficulty": task})
        run_episode(env, task)


if __name__ == "__main__":
    main()