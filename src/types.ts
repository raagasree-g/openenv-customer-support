export type Sentiment = 'Positive' | 'Neutral' | 'Negative' | 'Urgent';
export type Category = 'Billing' | 'Technical' | 'Account' | 'Feature Request' | 'General';
export type Action = 'Refund' | 'Escalate' | 'Reply' | 'Close' | 'Investigate';
export type Priority = 'Low' | 'Medium' | 'High' | 'Critical';

export interface SupportTicket {
  id: string;
  customerName: string;
  message: string;
  timestamp: string;
  status: 'Pending' | 'Processed';
  priority?: Priority;
  analysis?: {
    sentiment: Sentiment;
    sentimentScore: number;
    category: Category;
    confidence: number;
    suggestedAction: Action;
    reasoning: string;
    draftReply?: string;
  };
}

export const MOCK_SCENARIOS: (Partial<SupportTicket> & { label: string })[] = [
  {
    label: "Angry Billing",
    customerName: "Alex Rivera",
    message: "I've been charged twice for my subscription this month. This is unacceptable and I want my money back immediately!",
  },
  {
    label: "Feature Request",
    customerName: "Sarah Chen",
    message: "The new dashboard looks great! I was wondering if there's a way to export the data to CSV format?",
  },
  {
    label: "Tech Issue",
    customerName: "Michael Scott",
    message: "My login keeps failing with a 500 error. I've tried clearing my cache but nothing works. Please help, I have a big presentation in an hour.",
  },
  {
    label: "Happy Feedback",
    customerName: "Emily Blunt",
    message: "Just wanted to say thanks for the quick response on my last ticket. You guys are awesome!",
  }
];
