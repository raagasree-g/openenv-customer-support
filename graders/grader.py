def grade_episode(state):
    score = 0

    # correct issue detection
    if state.get("issue_type") == "delivery":
        score += 3

    # sentiment handling
    if state.get("sentiment") == "angry":
        score += 2

    # efficiency
    if state.get("time_elapsed", 10) <= 4:
        score += 2

    # business logic
    if state.get("customer_type") == "premium":
        score += 3

    return min(score, 10)