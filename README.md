# OpenEnv Customer Support Decision Engine (RL Environment)

This environment simulates real-world customer support decision-making where agents must balance customer satisfaction, cost, and uncertainty across multiple issues.

---

## 🚀 Problem Statement

Build an environment where an AI agent must:
- Understand customer queries
- Detect multiple hidden issues
- Choose actions (respond, refund, escalate)
- Balance business cost vs customer satisfaction

---

## 🧠 Core Idea

Unlike simple environments, this system forces agents to:

1. Detect multiple hidden issues from a single query  
2. Decide between competing actions (refund vs escalation vs response)  
3. Balance business cost against customer satisfaction  
4. Avoid inefficient or repetitive actions  

This creates a **non-trivial decision-making problem**, not a one-step solution.

---

## ⚙️ Actions

- `classify_issue`
- `detect_sentiment`
- `respond`
- `offer_refund`
- `escalate`

---

## 🔄 Interaction Flow

Agent → Action → Environment → Observation + Reward → Loop → Final Outcome

---

## 🔥 What Makes This Challenging?

Example:

**Query:**  
"I was charged twice and my order is delayed"

### ✅ Correct Behavior
- Detect BOTH payment + delivery issues  
- Choose appropriate resolution strategy  
- Avoid unnecessary cost  

### ❌ Incorrect Behavior
- Detect only one issue → partial failure  
- Refund unnecessarily → business loss  
- Delay response → customer dissatisfaction  

---

## ⚖️ Reward Design

- Partial rewards for correct intermediate steps  
- Penalties for skipping required steps  
- Cost-based penalties (refund vs escalation)  
- Time-based penalties for inefficiency  
- Failure penalties for incorrect decisions  

---

## 🌍 Real-World Factors Modeled

- Multi-issue customer queries  
- Customer sentiment (dynamic)  
- Customer type (premium vs normal)  
- Business cost trade-offs  
- Multi-step resolution process  

---

## 💡 Advanced Features

- Multi-issue detection (not single-label classification)  
- Decision branching with multiple valid strategies  
- Dynamic customer behavior (sentiment evolves)  
- Failure cases and penalties  
- Non-deterministic outcomes  

---

## ❌ Failure Cases

Agents can fail if they:
- Miss one of multiple issues  
- Choose costly or incorrect actions  
- Take too many steps  
- Repeat ineffective actions  

This ensures meaningful evaluation of agent performance.

---

## 📊 Evaluation Results

Baseline agent performance across multiple episodes:

Episode 1 → Score: 6.2  
Episode 2 → Score: 3.8  
Episode 3 → Score: 7.1  
Episode 4 → Score: 2.5 (failure case)  
Episode 5 → Score: 6.9  

**Average Score:** ~5.3  

This demonstrates:
- variability in outcomes  
- presence of failure cases  
- non-trivial decision-making complexity  

---

## ▶️ Example Run

Step 1 | classify_issue → Reward: +2  
Step 2 | detect_sentiment → Reward: +2  
Step 3 | respond → Reward: +3  

Final Score: 8/10  

---

## ▶️ How to Run

```bash
python inference.py