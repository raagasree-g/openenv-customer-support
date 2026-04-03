

from env import CustomerSupportEnv

env = CustomerSupportEnv()

# Reset environment
state = env.reset()
print("Initial State:")
print(state)

# Take one action
action = {"action_type": "classify_issue", "content": "delivery"}

state, reward, done, info = env.step(action)

print("\nAfter Step:")
print("State:", state)
print("Reward:", reward)
print("Done:", done)