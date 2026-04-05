from env import CustomerSupportEnv


# -------------------------
# AGENT LOGIC
# -------------------------
def get_agent_action(state):
    detected = state.get("detected_issues", [])
    sentiment = state.get("sentiment")

    # Step 1: detect issues
    if not detected:
        return {"action_type": "classify_issue"}

    # Step 2: detect sentiment
    if sentiment == "angry":
        return {
            "action_type": "respond",
            "content": "Sorry, we are resolving this urgently."
        }

    # Step 3: resolution decision
    if "payment" in detected:
        return {"action_type": "offer_refund"}

    return {"action_type": "respond", "content": "We are working on your issue."}


# -------------------------
# RUN SINGLE EPISODE
# -------------------------
def run_episode(env, episode_id):
    state = env.reset()
    done = False
    total_reward = 0
    step_count = 0
    MAX_STEPS = 10

    print(f"\n=== EPISODE {episode_id} ===")
    print("Customer Query:", state["customer_query"])
    print("Initial Sentiment:", state["sentiment"])
    print("-" * 50)

    while not done and step_count < MAX_STEPS:
        step_count += 1

        action = get_agent_action(state)

        result = env.step(action)

        state = result["observation"]
        reward = result["reward"]
        done = result["done"]

        total_reward += reward

        print(f"[STEP {step_count}]")
        print(f"Action: {action}")
        print(f"Reward: {reward:.2f}")
        print(f"Detected Issues: {state.get('detected_issues')}")
        print(f"Sentiment: {state.get('sentiment')}")
        print("-" * 30)

    # -------------------------
    # FINAL STATUS
    # -------------------------
    if state.get("resolved"):
        print("✅ RESOLVED")
    else:
        print("❌ FAILED")

    print(f"Total Reward: {total_reward:.2f}")
    print("=" * 50)

    return total_reward, state


# -------------------------
# MULTI-EPISODE EVALUATION
# -------------------------
def evaluate_agent(env, num_episodes=5):
    scores = []
    successes = 0

    for i in range(1, num_episodes + 1):
        score, state = run_episode(env, i)
        scores.append(score)

        if state.get("resolved"):
            successes += 1

    avg_score = sum(scores) / len(scores)

    print("\n===== FINAL EVALUATION =====")
    print(f"Episodes: {num_episodes}")
    print(f"Success Rate: {successes}/{num_episodes}")
    print(f"Average Score: {avg_score:.2f}")
    print("============================\n")


# -------------------------
# MAIN
# -------------------------
def main():
    env = CustomerSupportEnv()

    print("🚀 Starting Customer Support Environment Evaluation")

    evaluate_agent(env, num_episodes=5)


if __name__ == "__main__":
    main()