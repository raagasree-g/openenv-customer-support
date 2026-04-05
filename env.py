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
        import random

        reward = 0
        done = False

        action_type = action.get("action_type")
        content = action.get("content", "")

        # -------------------------
        # MEMORY PENALTY
        # -------------------------
        repeat_count = self.state_data["history"].count(action_type)
        if repeat_count > 0:
            reward -= (1 + 0.5 * repeat_count)

        # -------------------------
        # TIME PENALTY
        # -------------------------
        reward -= 0.2

        # -------------------------
        # TRACK ATTEMPTS
        # -------------------------
        self.state_data["attempts"] += 1

        # -------------------------
        # FAILURE CONDITION
        # -------------------------
        if self.state_data["attempts"] > 5:
            return {
                "observation": self.state_data,
                "reward": -5,
                "done": True,
                "info": {
                    "attempts": self.state_data["attempts"],
                    "time_elapsed": self.state_data["time_elapsed"]
                }
            }

        query = self.state_data["customer_query"].lower()

        # -------------------------
        # ACTION LOGIC
        # -------------------------

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

            detected = list(set(detected))
            self.state_data["detected_issues"] = detected

            true_set = set(self.state_data["true_issues"])
            detected_set = set(detected)

            correct = detected_set & true_set
            wrong = detected_set - true_set

            reward += len(correct) * 2
            reward -= len(wrong) * 1.5

            if len(detected_set) == 0:
                reward -= 2

        elif action_type == "detect_sentiment":
            if content == self.state_data["sentiment"]:
                reward += 2
            else:
                reward -= 1.5

        elif action_type == "respond":
            if "sorry" in content.lower():
                self.state_data["sentiment"] = "calm"
                reward += 1
            else:
                self.state_data["sentiment"] = "angry"
                reward -= 1

        elif action_type == "offer_refund":
            if "payment" in self.state_data["true_issues"]:
                if random.random() < 0.85:
                    reward += 3
                else:
                    reward -= 2
            else:
                reward -= 4

            reward -= 0.5  # cost

        elif action_type == "escalate":
            if self.state_data["sentiment"] == "angry":
                reward += 1
            else:
                reward -= 3

            reward -= 0.3  # cost

        else:
            reward -= 2

        # -------------------------
        # WRONG RESOLUTION PENALTY
        # -------------------------
        if action_type in ["respond", "offer_refund"]:
            if set(self.state_data["detected_issues"]) != set(self.state_data["true_issues"]):
                reward -= 3

        # -------------------------
        # SUCCESS CONDITION
        # -------------------------
        if set(self.state_data["detected_issues"]) == set(self.state_data["true_issues"]):
            if action_type in ["respond", "offer_refund"]:
                self.state_data["resolved"] = True
                done = True
                reward += 3

        # -------------------------
        # UPDATE STATE
        # -------------------------
        self.state_data["history"].append(action_type)
        self.state_data["time_elapsed"] += 1

        # -------------------------
        # RETURN FORMAT (IMPORTANT)
        # -------------------------
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