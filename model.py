import re
import json
import os
from datetime import datetime

class SupportAgentModel:
    """
    Aegis-7 Heuristic Decision Engine (Python Implementation)
    
    This class implements the core logic for the SupportAgent AI.
    It uses a combination of pattern matching, sentiment analysis,
    and a heuristic decision tree to classify and analyze support tickets.
    """
    
    def __init__(self, weights_path="model_metadata.json"):
        self.version = "2.4.0-STABLE"
        self.engine = "Aegis-7 Heuristic"
        
        # Default heuristic weights (can be updated via training)
        self.weights = {
            "sentiment_threshold": 0.6,
            "confidence_base": 0.85,
            "latency_target_ms": 140
        }
        
        if os.path.exists(weights_path):
            try:
                with open(weights_path, "r") as f:
                    self.weights.update(json.load(f))
            except Exception:
                pass

        # Category Patterns
        self.category_patterns = {
            "Billing": r"(?i)(billing|payment|invoice|charge|refund|price|cost|subscription|card|credit|debit)",
            "Technical": r"(?i)(technical|error|bug|crash|fail|broken|issue|not working|slow|performance|api|integration)",
            "Account": r"(?i)(account|login|password|access|permission|profile|security|mfa|2fa|reset|email)",
            "Feature Request": r"(?i)(feature|request|add|improvement|suggestion|wishlist|could you|would be nice)"
        }
        
        # Sentiment Markers
        self.sentiment_markers = {
            "negative": ["angry", "frustrated", "bad", "terrible", "awful", "worst", "hate", "disappointed", "annoyed", "useless"],
            "positive": ["happy", "great", "excellent", "good", "thanks", "thank you", "love", "perfect", "helpful", "awesome"],
            "urgent": ["urgent", "asap", "immediately", "emergency", "critical", "broken", "down", "stop", "help", "now"]
        }

    def analyze(self, text):
        """
        Analyzes the input text and returns a structured decision object.
        """
        start_time = datetime.now()
        
        # 1. Sentiment Analysis
        sentiment, score = self._analyze_sentiment(text)
        
        # 2. Category Classification
        category = self._classify_category(text)
        
        # 3. Confidence Calculation
        confidence = self.weights.get("confidence_base", 0.85) + (score * 0.1)
        
        # 4. Suggested Action & Reasoning
        action, reasoning = self._determine_action(sentiment, category, text)
        
        # 5. Draft Reply
        draft = self._generate_draft(sentiment, category, action)
        
        end_time = datetime.now()
        latency_ms = (end_time - start_time).total_seconds() * 1000
        
        return {
            "sentiment": sentiment,
            "sentimentScore": score,
            "category": category,
            "confidence": min(confidence, 0.99),
            "suggestedAction": action,
            "reasoning": reasoning,
            "draftReply": draft,
            "metadata": {
                "engine": self.engine,
                "version": self.version,
                "latency_ms": latency_ms,
                "timestamp": datetime.now().isoformat()
            }
        }

    def _analyze_sentiment(self, text):
        text_lower = text.lower()
        neg_count = sum(1 for m in self.sentiment_markers["negative"] if m in text_lower)
        pos_count = sum(1 for m in self.sentiment_markers["positive"] if m in text_lower)
        urg_count = sum(1 for m in self.sentiment_markers["urgent"] if m in text_lower)
        
        if urg_count > 0 or "!" in text:
            return "Urgent", 0.9
        if neg_count > pos_count:
            return "Negative", 0.7 + (neg_count * 0.05)
        if pos_count > neg_count:
            return "Positive", 0.7 + (pos_count * 0.05)
        return "Neutral", 0.5

    def _classify_category(self, text):
        for category, pattern in self.category_patterns.items():
            if re.search(pattern, text):
                return category
        return "General"

    def _determine_action(self, sentiment, category, text):
        if sentiment == "Urgent":
            return "Escalate", "High priority detected due to urgency markers or punctuation."
        if category == "Billing" and "refund" in text.lower():
            return "Refund", "Customer explicitly requested a refund for a billing issue."
        if category == "Technical":
            return "Escalate", "Technical issues require specialist intervention for debugging."
        if sentiment == "Negative":
            return "Escalate", "Negative sentiment detected, human touch recommended for de-escalation."
        return "Close", "Standard inquiry resolved or information provided."

    def _generate_draft(self, sentiment, category, action):
        if action == "Escalate":
            return "I've escalated your ticket to our senior support team. They will review the details and get back to you shortly."
        if action == "Refund":
            return "I've initiated a refund request for your recent transaction. You should see it in your account within 3-5 business days."
        return "Thank you for reaching out! I've processed your request. Is there anything else I can help you with?"

if __name__ == "__main__":
    agent = SupportAgentModel()
    result = agent.analyze("I am very frustrated with the billing error on my account! I need a refund immediately.")
    print(json.dumps(result, indent=2))
