"""
Interactive Chatbot with Conversation Management

Features:
- Multi-turn conversation support
- Context awareness
- Response generation with emotional awareness
- Modular architecture for easy expansion

Author: Assignment Solution
Date: 2025
"""

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
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
            
        Returns:
            Message dictionary with timestamp
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

        # Get last user and assistant messages for context
        user_messages = [
            msg for msg in self.conversation_history if msg['role'] == 'user'
        ]
        
        if user_messages:
            return user_messages[-1]['content']
        return ""

    def generate_response(self, user_input: str) -> str:
        """
        Generate a contextually appropriate response
        
        Args:
            user_input: The user's message
            
        Returns:
            Chatbot's response
        """
        # Response templates for different scenarios
        responses = {
            'greeting': [
                "Hello! I'm here to help. What's on your mind?",
                "Hi there! How can I assist you today?",
                "Welcome! I'm ready to listen and help.",
            ],
            'question': [
                "That's an interesting question. Let me think about that.",
                "I appreciate you asking. Here's my perspective:",
                "Great question! Here's what I think:",
            ],
            'complaint': [
                "I understand your frustration. Let me see how I can help.",
                "I'm sorry to hear that. Your concern is important to me.",
                "I understand how you feel. Let's work through this together.",
            ],
            'positive': [
                "That's wonderful to hear!",
                "I'm glad you're happy with that!",
                "That's great! I appreciate the positive feedback.",
            ],
            'default': [
                "Thank you for sharing that with me.",
                "I understand. Tell me more about that.",
                "That's helpful to know. How else can I assist?",
            ]
        }

        # Detect message type
        lower_input = user_input.lower()
        
        if any(word in lower_input for word in ['hello', 'hi', 'hey', 'greetings']):
            category = 'greeting'
        elif any(word in lower_input for word in ['?', 'what', 'how', 'why', 'when', 'where']):
            category = 'question'
        elif any(word in lower_input for word in ['bad', 'terrible', 'awful', 'hate', 'disappointing', 'disappointed', 'frustrat']):
            category = 'complaint'
        elif any(word in lower_input for word in ['good', 'great', 'love', 'excellent', 'wonderful', 'amazing', 'fantastic']):
            category = 'positive'
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
