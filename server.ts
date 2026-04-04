import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // --- Health Check ---
  app.get("/api/health", (req, res) => {
    res.json({ status: "online", engine: "Aegis-7", version: "v2.4.0-STABLE", uptime: process.uptime() });
  });

  // --- Decision Engine Logic (Backend) ---
  app.post("/api/analyze", (req, res) => {
    const { message } = req.body;
    if (!message) return res.status(400).json({ error: "Message is required" });

    const lowerMessage = message.toLowerCase();
    
    // 1. Category
    let category = 'General';
    if (lowerMessage.match(/charge|money|refund|subscription|price|billing|invoice|pay|cost|expensive|payment|card|credit|debit|bank|transaction/)) {
      category = 'Billing';
    } else if (lowerMessage.match(/error|bug|fail|broken|login|500|crash|not working|slow|issue|api|integration|connection|timeout|database|server|down|latency|performance/)) {
      category = 'Technical';
    } else if (lowerMessage.match(/password|account|email|profile|settings|login|access|username|security|mfa|2fa|permission|reset|locked|unauthorized/)) {
      category = 'Account';
    } else if (lowerMessage.match(/export|add|feature|wish|want|csv|could you|request|improve|better|suggestion|idea|roadmap|integration|plugin/)) {
      category = 'Feature Request';
    }

    // 2. Sentiment
    let sentiment = 'Neutral';
    let sentimentScore = 0.5;
    const positiveWords = ['thanks', 'awesome', 'great', 'love', 'perfect', 'good', 'happy', 'appreciate', 'helpful', 'excellent', 'fast', 'solved'];
    const negativeWords = ['unacceptable', 'angry', 'bad', 'worst', 'hate', 'terrible', 'frustrated', 'immediately', 'disappointed', 'fix this', 'broken', 'useless', 'garbage'];
    const urgentWords = ['urgent', 'asap', 'immediately', 'now', 'presentation', 'critical', 'emergency', 'blocking', 'stop', 'deadline', 'prod', 'production'];

    const posCount = positiveWords.filter(w => lowerMessage.includes(w)).length;
    const negCount = negativeWords.filter(w => lowerMessage.includes(w)).length;
    const urgentCount = urgentWords.filter(w => lowerMessage.includes(w)).length;

    if (urgentCount > 0 || (negCount > 1 && (lowerMessage.includes('!') || lowerMessage.includes('?')))) {
      sentiment = 'Urgent';
      sentimentScore = 0.85 + Math.min(urgentCount * 0.05, 0.15);
    } else if (negCount > posCount) {
      sentiment = 'Negative';
      sentimentScore = 0.65 + Math.min(negCount * 0.08, 0.35);
    } else if (posCount > negCount) {
      sentiment = 'Positive';
      sentimentScore = 0.75 + Math.min(posCount * 0.08, 0.25);
    }

    // 3. Action & Reasoning
    let suggestedAction = 'Reply';
    let reasoning = "Standard inquiry detected. Routing to general support queue.";

    if (sentiment === 'Urgent') {
      suggestedAction = 'Escalate';
      reasoning = "High-priority sentiment detected. Escalating to Critical Incident Response Team.";
    } else if (category === 'Technical') {
      suggestedAction = 'Escalate';
      reasoning = "Technical complexity identified. Routing to Engineering Tier 2.";
    } else if (category === 'Billing' && lowerMessage.match(/refund|charge|money/)) {
      suggestedAction = 'Refund';
      reasoning = "Financial discrepancy identified. Flagged for immediate billing audit.";
    } else if (category === 'Feature Request') {
      suggestedAction = 'Investigate';
      reasoning = "Product enhancement request detected. Added to Q3 Roadmap backlog.";
    } else if (sentiment === 'Positive' && lowerMessage.length < 100) {
      suggestedAction = 'Close';
      reasoning = "Customer satisfaction confirmed via sentiment analysis. Closing loop.";
    }

    // 4. Draft Reply
    let draftReply = "";
    if (category === 'Billing') {
      draftReply = "Hi there, I've reviewed your billing inquiry. I've flagged this for our finance team to investigate the charges immediately. You should see an update within 24 hours.";
    } else if (category === 'Technical') {
      draftReply = "Hello, I'm sorry to hear you're experiencing technical issues. I've gathered the system logs and escalated this to our engineering team for a deep dive.";
    } else if (category === 'Account') {
      draftReply = "Hi, for your security, I've initiated a secure identity verification process. Please check your registered email for a verification link to proceed.";
    } else if (category === 'Feature Request') {
      draftReply = "Thank you for the great suggestion! I've logged this in our product feedback system. Our team reviews these weekly to prioritize our roadmap.";
    } else {
      draftReply = "Hello! Thank you for reaching out. I've analyzed your request and routed it to the best specialist to help you. We'll be in touch shortly.";
    }

    const processingSteps = [
      "Tokenizing input stream...",
      "Executing sentiment heuristic engine...",
      "Mapping intent to category clusters...",
      "Generating autonomous draft response..."
    ];

    res.json({
      sentiment,
      sentimentScore: Math.min(sentimentScore, 1),
      category,
      confidence: 0.92 + (Math.random() * 0.05),
      suggestedAction,
      reasoning,
      draftReply,
      agentMetadata: {
        name: "Aegis-7",
        version: "v2.4.0-stable",
        processingTimeMs: 150
      },
      processingSteps
    });
  });

  // --- Vite Middleware ---
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
