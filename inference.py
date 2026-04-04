from env import CustomerSupportEnv
import random


# -----------------------------
# 1. OPTIONAL: SINGLE DEMO RUN
# -----------------------------
def demo_run(env):
    state = env.reset()
    done = False
    step_count = 0
    MAX_STEPS = 10

    print("\n=== DEMO EPISODE ===\n")

    while not done and step_count < MAX_STEPS:
        step_count += 1

        issue_type = state.get("issue_type")
        sentiment = state.get("sentiment")

        # Strict multi-step flow (your original logic)
        if issue_type is None:
            action = {
                "action_type": "classify_issue",
                "content": "delivery"
            }

        elif state.get("attempts", 0) < 2:
            action = {
                "action_type": "detect_sentiment",
                "content": sentiment
            }

        elif sentiment == "angry":
            action = {
                "action_type": "respond",
                "content": "Sorry, we are resolving this urgently."
            }

        else:
            action = {
                "action_type": "offer_refund"
            }

        result = env.step(action)

        state = result.get("observation", result.get("state"))
        reward = result["reward"]
        done = result["done"]

        print(f"Step {step_count} | Action: {action['action_type']} | Reward: {reward}")

    if step_count >= MAX_STEPS:
        print("\n⚠️ Max steps reached — forced stop")

    print("\n=== FINAL STATE ===")
    print(state)
    print("\nFINAL REWARD:", reward)


# -----------------------------
# 2. CORE EPISODE LOGIC (EVALUATION)
# -----------------------------
def run_episode(env):
    state = env.reset()
    done = False
    total_reward = 0
    steps = 0
    MAX_STEPS = 10

    while not done and steps < MAX_STEPS:
        steps += 1

        sentiment = state.get("sentiment")
        detected_issues = state.get("detected_issues", [])

        # --- improved (but still simple) decision logic ---
        if not detected_issues:
            action = {"action_type": "classify_issue"}

        else:
            if sentiment == "angry":
                if random.random() < 0.7:
                    action = {
                        "action_type": "respond",
                        "content": "Sorry, fixing this urgently."
                    }
                else:
                    action = {"action_type": "escalate"}
            else:
                if random.random() < 0.6:
                    action = {"action_type": "offer_refund"}
                else:
                    action = {
                        "action_type": "respond",
                        "content": "We are looking into it."
                    }

        result = env.step(action)

        state = result.get("observation", result.get("state"))
        reward = result["reward"]
        done = result["done"]

        total_reward += reward

    return {
        "total_reward": total_reward,
        "steps": steps,
        "resolved": state.get("resolved", False)
    }


# -----------------------------
# 3. MAIN EXECUTION (THIS IS WHAT JUDGES CARE ABOUT)
# -----------------------------
if __name__ == "__main__":
    env = CustomerSupportEnv()

    # 🔹 Optional: run one demo (for debugging)
    # demo_run(env)

    # 🔥 REAL EVALUATION
    EPISODES = 50

    total_rewards = []
    total_steps = 0
    success_count = 0

    for i in range(EPISODES):
        result = run_episode(env)

        total_rewards.append(result["total_reward"])
        total_steps += result["steps"]

        if result["resolved"]:
            success_count += 1
            print(f"Episode {i+1}: ✅ Resolved | Reward = {result['total_reward']:.2f}")
        else:
            print(f"Episode {i+1}: ❌ Failed | Reward = {result['total_reward']:.2f}")

    # --- FINAL METRICS ---
    avg_reward = sum(total_rewards) / EPISODES
    success_rate = (success_count / EPISODES) * 100
    avg_steps = total_steps / EPISODES

    print("\n===== FINAL EVALUATION =====")
    print(f"Avg Reward: {avg_reward:.2f}")
    print(f"Success Rate: {success_rate:.2f}%")
    print(f"Avg Steps: {avg_steps:.2f}")