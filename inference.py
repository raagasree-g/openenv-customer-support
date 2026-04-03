from env import CustomerSupportEnv

env = CustomerSupportEnv()
state = env.reset()

done = False
step_count = 0
MAX_STEPS = 10   # safety limit

print("\n=== STARTING EPISODE ===\n")

while not done and step_count < MAX_STEPS:
    step_count += 1

    issue_type = state.get("issue_type")
    sentiment = state.get("sentiment")

    # ✅ STRICT multi-step flow (matches env rules)
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

    # ✅ NEW return format
    result = env.step(action)

    state = result["observation"]
    reward = result["reward"]
    done = result["done"]

    print(f"Step {step_count} | Action: {action['action_type']} | Reward: {reward}")

# Safety exit
if step_count >= MAX_STEPS:
    print("\n⚠️ Max steps reached — forced stop")

print("\n=== FINAL STATE ===")
print(state)
print("\nFINAL SCORE:", reward)