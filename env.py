class CustomerSupportEnv:

    def __init__(self):
        self.state_data = {}

    def reset(self):
        import random

        queries = [
            {
                "text": "My order is delayed and I was charged twice",
                "true_issues": ["delivery", "payment"]
            },
            {
                "text": "I got a damaged product and support is not responding",
                "true_issues": ["product", "support"]
            },
            {
                "text": "My payment failed but money got deducted",
                "true_issues": ["payment"]
            }
        ]

        sample = random.choice(queries)

        self.state_data = {
            "customer_query": sample["text"],
            "true_issues": sample["true_issues"],
            "detected_issues": [],

            "customer_type": random.choice(["normal", "premium"]),
            "sentiment": random.choice(["calm", "angry"]),

            "history": [],
            "time_elapsed": 0,
            "resolved": False,
            "attempts": 0
        }

        return self.state_data

    def step(self, action):
        reward = 0
        done = False
        info = {}

        action_type = action.get("action_type")
        content = action.get("content", "")

        # ✅ FIXED INDENTATION STARTS HERE
        self.state_data["attempts"] += 1

        # 🚨 FAILURE CONDITION
        if self.state_data["attempts"] > 4:
            reward = -5
            done = True

            return {
                "observation": self.state_data,
                "reward": reward,
                "done": done,
                "info": {
                    "attempts": self.state_data.get("attempts"),
                    "time_elapsed": self.state_data.get("time_elapsed")
                }
            }

        # CONTINUE FLOW
        query = self.state_data.get("customer_query", "").lower()

        if action_type == "classify_issue":
            detected = []

            if "order" in query or "delay" in query:
                detected.append("delivery")

            if "charged" in query or "payment" in query:
                detected.append("payment")

            if "damaged" in query:
                detected.append("product")

            if "support" in query:
                detected.append("support")

            self.state_data["detected_issues"] = list(set(detected))

            correct = set(detected) & set(self.state_data["true_issues"])
            reward += len(correct) * 2

            if len(self.state_data["detected_issues"]) == 0:
                reward -= 2

        elif action_type == "detect_sentiment":
            if content == self.state_data.get("sentiment"):
                reward += 2
            else:
                reward -= 1

        elif action_type == "respond":
            if "sorry" in content.lower():
                self.state_data["sentiment"] = "calm"
                reward += 1
            else:
                self.state_data["sentiment"] = "angry"
                reward -= 1

        elif action_type == "offer_refund":
            if "payment" in self.state_data["true_issues"]:
                reward += 3
            else:
                reward -= 4

        elif action_type == "escalate":
            if self.state_data["sentiment"] == "angry":
                reward += 1
            else:
                reward -= 3

        if set(self.state_data["detected_issues"]) == set(self.state_data["true_issues"]):
            if action_type in ["respond", "offer_refund"]:
                self.state_data["resolved"] = True
                done = True
                reward += 3

        self.state_data["history"].append(action_type)
        self.state_data["time_elapsed"] += 1

        return {
            "observation": self.state_data,
            "reward": reward,
            "done": done,
            "info": {
                "attempts": self.state_data["attempts"],
                "time_elapsed": self.state_data["time_elapsed"]
            }
        }

    def state(self):
        return self.state_data