
from typing import List, Dict
import random
from datetime import datetime


class Chatbot:
    """Modular chatbot with conversation management"""

    def __init__(self, name: str = "SentimentBot"):
        """
        Initialize the chatbot
        
        Args:
            name: Name of the chatbot
        """
        self.name = name
        self.conversation_history = []
        self.start_time = datetime.now()

    def add_message(self, role: str, content: str) -> Dict:
        """
        Add a message to conversation history
        """
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        self.conversation_history.append(message)
        return message

    def get_history(self) -> List[Dict]:
        """Return conversation history"""
        return self.conversation_history

    def get_context(self) -> str:
        """Extract context from recent messages"""
        if len(self.conversation_history) < 2:
            return "Start of conversation"

        user_messages = [
            msg for msg in self.conversation_history if msg['role'] == 'user'
        ]
        
        if user_messages:
            return user_messages[-1]['content']
        return ""

    def generate_response(self, user_input: str, sentiment_label: str = None) -> str:
        """
        Generate a contextually appropriate response with sentiment awareness
        """
        # Response templates for different sentiment categories
        responses = {
            'negative_empathy': [
                "I’m sorry to hear that. I’ll make sure your concern is addressed.",
                "I understand this didn’t meet your expectations. I’m here to help fix it.",
                "I’m sorry you feel this way. Let me try to make things better.",
            ],
            'negative_support': [
                "I hear your disappointment. Let me help you find a solution.",
                "I’m sorry things didn’t go well. What can we improve?",
                "Your concern is valid. Tell me how I can support you.",
            ],
            'positive_celebration': [
                "I’m glad to hear that! I’ll continue to keep up that standard.",
                "That’s wonderful! I’m happy your experience was better.",
                "Great! I’m happy things are improving for you.",
            ],
            'positive_encouragement': [
                "That’s great! I appreciate the positive feedback.",
                "Awesome! I’m glad things are moving in the right direction.",
                "Good to hear! Let me know how else I can help.",
            ],
            'neutral_inquiry': [
                "I see. Could you tell me more?",
                "Alright. What would you like to discuss further?",
                "Okay. How can I assist you next?",
            ],
            'neutral_acknowledge': [
                "Thank you for sharing that.",
                "Got it. Let me know what you'd like to do next.",
                "Okay, I understand.",
            ],
            'default': [
                "I’m here to help. Tell me more.",
                "Alright. How would you like to continue?",
                "I’m listening. Go ahead.",
            ]
        }

        lower_input = user_input.lower()

        # Sentiment-based selection
        if sentiment_label == "NEGATIVE":
            if any(word in lower_input for word in ['help', 'can', 'support', 'fix', 'solve']):
                category = 'negative_support'
            else:
                category = 'negative_empathy'

        elif sentiment_label == "POSITIVE":
            if any(word in lower_input for word in ['excited', 'happy', 'love', 'amazing', 'fantastic', 'wonderful']):
                category = 'positive_celebration'
            else:
                category = 'positive_encouragement'

        elif sentiment_label == "NEUTRAL":
            if any(word in lower_input for word in ['?', 'what', 'how', 'why', 'when', 'where']):
                category = 'neutral_inquiry'
            else:
                category = 'neutral_acknowledge'

        else:
            # Fallback keyword-based detection
            if any(word in lower_input for word in ['hello', 'hi', 'hey', 'greetings']):
                category = 'neutral_inquiry'
            elif any(word in lower_input for word in ['bad', 'terrible', 'awful', 'hate', 'disappointing', 'frustrated']):
                category = 'negative_empathy'
            elif any(word in lower_input for word in ['good', 'great', 'love', 'excellent', 'wonderful', 'amazing', 'fantastic']):
                category = 'positive_celebration'
            else:
                category = 'default'

        return random.choice(responses[category])

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.start_time = datetime.now()

    def get_summary(self) -> Dict:
        """Get conversation summary statistics"""
        total_messages = len(self.conversation_history)
        user_messages = sum(1 for msg in self.conversation_history if msg['role'] == 'user')
        assistant_messages = total_messages - user_messages

        return {
            'total_messages': total_messages,
            'user_messages': user_messages,
            'assistant_messages': assistant_messages,
            'duration': str(datetime.now() - self.start_time)
        }
