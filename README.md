# AI Customer Support Decision Engine

## Description
Simulates a customer support environment where an agent must classify issues, detect sentiment, and take actions.

## Actions
- classify_issue
- detect_sentiment
- respond
- offer_refund
- escalate

## How to Run
python inference.py

## Reward Design
- Partial rewards for correct steps
- Penalties for skipping steps
- Time-based penalty for inefficiency

## Real-world Factors
- Customer type affects decisions
- Cost of refund vs escalation
- Multi-step resolution required

## Environment Design

This environment simulates real-world customer support decision-making with:

- Multi-step reasoning (classification → sentiment → resolution)
- Partial reward shaping (not binary success/failure)
- Business cost modeling (refund vs escalation trade-offs)
- Time-based penalties for inefficiency

## Why This Matters

Unlike simple environments, this system evaluates:

- decision quality over multiple steps
- trade-offs between customer satisfaction and cost
- realistic agent behavior in support scenarios

## Example Run

Step 1 | classify_issue → Reward: +2  
Step 2 | detect_sentiment → Reward: +2  
Step 3 | respond → Reward: +3  

Final Score: 8/10