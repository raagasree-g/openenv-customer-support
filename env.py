class CustomerSupportEnv:

    def __init__(self):
        self.state_data = {}

    def reset(self):
        import random

        queries = [
            "My order is delayed",
            "I got a damaged product",
            "I want a refund immediately",
            "My payment failed but money deducted"
        ]

        self.state_data = {
            "customer_query": random.choice(queries),
            "customer_type": random.choice(["normal", "premium"]),
            "sentiment": random.choice(["calm", "angry"]),

            "issue_type": None,
            "true_issue": random.choice(["delivery", "other"]),  # hidden truth

            "history": [],
            "time_elapsed": 0,

            "resolved": False,   # Step 6
            "attempts": 0        # Step 6
        }

        return self.state_data

    def step(self, action):
        reward = 0
        done = False
        info = {}

        action_type = action.get("action_type")
        content = action.get("content", "")

        # ✅ track attempts
        self.state_data["attempts"] += 1

        query = self.state_data.get("customer_query", "").lower()

        # ⛔ penalty for skipping steps
        if action_type in ["respond", "offer_refund"] and self.state_data.get("issue_type") is None:
            reward = -3
            return {
    "observation": self.state_data,
    "reward": reward,
    "done": done,
    "info": {
        "attempts": self.state_data.get("attempts"),
        "time_elapsed": self.state_data.get("time_elapsed")
    }
}

        # STEP 1: classify issue (uses hidden truth now)
        if action_type == "classify_issue":
            if self.state_data["true_issue"] == "delivery":
                self.state_data["issue_type"] = "delivery"
                reward = 2
            else:
                self.state_data["issue_type"] = "other"
                reward = 1

        # STEP 2: detect sentiment
        elif action_type == "detect_sentiment":
            if content == self.state_data.get("sentiment"):
                reward = 2
            else:
                reward = -1

        # STEP 3: respond / refund (multi-turn enforced)
        elif action_type in ["respond", "offer_refund"]:
            if self.state_data["attempts"] >= 2:
                self.state_data["resolved"] = True
                done = True

                if action_type == "offer_refund" and self.state_data.get("issue_type") == "delivery":
                    reward = 3
                else:
                    reward = 2
            else:
                reward = -1  # too early to resolve

        # STEP 4: optional escalation
        elif action_type == "escalate":
            reward = 1

        # ❌ WRONG ACTION PENALTIES
        if action_type == "offer_refund" and self.state_data["customer_type"] == "normal":
            reward -= 3

        if action_type == "escalate" and self.state_data["sentiment"] == "calm":
            reward -= 2

        # 💰 BUSINESS COST SYSTEM
        cost = 0
        if action_type == "offer_refund":
            cost = 5
        elif action_type == "escalate":
            cost = 3

        reward -= cost * 0.5

        # track history + time
        self.state_data["history"].append(action_type)
        self.state_data["time_elapsed"] += 1

        return {
    "observation": self.state_data,
    "reward": reward,
    "done": done,
    "info": {
        "attempts": self.state_data.get("attempts"),
        "time_elapsed": self.state_data.get("time_elapsed")
    }
}
    def state(self):
        return self.state_data