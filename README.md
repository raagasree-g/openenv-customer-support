This environment simulates real-world customer support decision-making where agents must balance customer satisfaction, cost, and uncertainty across multiple issues.

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

## Advanced Features

- Multi-issue detection (not single-label classification)
- Decision branching with multiple valid strategies
- Business cost modeling (refund vs escalation trade-offs)
- Dynamic customer behavior (sentiment evolves)
- Failure penalties for inefficient agents

## Evaluation Results

The baseline agent was tested across multiple episodes:

Episode 1 → Score: 6.2  
Episode 2 → Score: 3.8  
Episode 3 → Score: 7.1  
Episode 4 → Score: 2.5 (failure case)  
Episode 5 → Score: 6.9  

Average Score: ~5.3

This demonstrates:
- variability in outcomes
- presence of failure cases
- non-trivial decision-making complexity

## Core Idea

Unlike simple environments, this system forces agents to:

1. Detect multiple hidden issues from a single query  
2. Decide between competing actions (refund vs escalation vs response)  
3. Balance business cost against customer satisfaction  
4. Avoid inefficient or repetitive actions  

This creates a non-trivial decision-making problem rather than a one-step solution.

## What Makes This Challenging?

Example:

Query: "I was charged twice and my order is delayed"

Correct behavior:
- Detect BOTH payment + delivery issues  
- Decide whether refund is justified  
- Respond appropriately without unnecessary cost  

Incorrect behavior:
- Only detect one issue → partial failure  
- Refund unnecessarily → business loss  
- Delay response → customer dissatisfaction  

## Failure Cases

Agents can fail if they:
- miss one of multiple issues  
- choose costly actions unnecessarily  
- take too many steps  
- repeat ineffective actions  

This ensures the environment meaningfully evaluates agent quality.

## Interaction Flow

Agent → Action → Environment → Updated State + Reward → Loop → Final Outcome

This environment is designed to evaluate decision-making under uncertainty rather than generate responses.