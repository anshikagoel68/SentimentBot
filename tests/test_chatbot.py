"""
Comprehensive tests for Chatbot functionality
Tests conversation management and response generation

Author: Assignment Solution
Date: 2025
"""

import unittest
from chatbot import Chatbot


class TestChatbot(unittest.TestCase):
    """Test suite for chatbot functionality"""

    def setUp(self):
        """Initialize chatbot for each test"""
        self.chatbot = Chatbot(name="TestBot")

    def test_chatbot_initialization(self):
        """Test chatbot initializes correctly"""
        self.assertEqual(self.chatbot.name, "TestBot")
        self.assertEqual(len(self.chatbot.get_history()), 0)

    def test_add_user_message(self):
        """Test adding user message to history"""
        self.chatbot.add_message('user', 'Hello')
        history = self.chatbot.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['role'], 'user')
        self.assertEqual(history[0]['content'], 'Hello')

    def test_add_assistant_message(self):
        """Test adding assistant message to history"""
        self.chatbot.add_message('assistant', 'Hi there!')
        history = self.chatbot.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['role'], 'assistant')

    def test_multi_turn_conversation(self):
        """Test multi-turn conversation"""
        self.chatbot.add_message('user', 'Hello')
        self.chatbot.add_message('assistant', 'Hi!')
        self.chatbot.add_message('user', 'How are you?')
        self.chatbot.add_message('assistant', 'I am great!')
        
        history = self.chatbot.get_history()
        self.assertEqual(len(history), 4)

    def test_message_has_timestamp(self):
        """Test that messages include timestamp"""
        msg = self.chatbot.add_message('user', 'Test')
        self.assertIn('timestamp', msg)

    def test_generate_response_greeting(self):
        """Test response generation for greeting"""
        response = self.chatbot.generate_response('hello')
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_generate_response_question(self):
        """Test response generation for question"""
        response = self.chatbot.generate_response('What is your name?')
        self.assertIsNotNone(response)
        self.assertIn("think", response.lower())

    def test_generate_response_complaint(self):
        """Test response generation for complaint"""
        response = self.chatbot.generate_response('This is terrible!')
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)

    def test_generate_response_positive(self):
        """Test response generation for positive message"""
        response = self.chatbot.generate_response('That is wonderful!')
        self.assertIsNotNone(response)

    def test_get_context(self):
        """Test context extraction"""
        self.chatbot.add_message('user', 'First message')
        self.chatbot.add_message('assistant', 'Response')
        self.chatbot.add_message('user', 'Second message')
        
        context = self.chatbot.get_context()
        self.assertEqual(context, 'Second message')

    def test_clear_history(self):
        """Test clearing conversation history"""
        self.chatbot.add_message('user', 'Hello')
        self.chatbot.add_message('assistant', 'Hi')
        
        self.chatbot.clear_history()
        self.assertEqual(len(self.chatbot.get_history()), 0)

    def test_get_summary(self):
        """Test conversation summary"""
        self.chatbot.add_message('user', 'Hello')
        self.chatbot.add_message('assistant', 'Hi')
        self.chatbot.add_message('user', 'How are you?')
        
        summary = self.chatbot.get_summary()
        self.assertEqual(summary['total_messages'], 3)
        self.assertEqual(summary['user_messages'], 2)
        self.assertEqual(summary['assistant_messages'], 1)

    def test_response_variety(self):
        """Test that responses have variety"""
        responses = set()
        for _ in range(10):
            response = self.chatbot.generate_response('hello')
            responses.add(response)
        
        # Should have multiple different responses
        self.assertGreater(len(responses), 1)

    def test_empty_message_content(self):
        """Test handling of empty message content"""
        msg = self.chatbot.add_message('user', '')
        self.assertEqual(msg['content'], '')

    def test_long_message(self):
        """Test handling of very long messages"""
        long_text = 'a' * 1000
        msg = self.chatbot.add_message('user', long_text)
        self.assertEqual(msg['content'], long_text)


if __name__ == '__main__':
    unittest.main()
