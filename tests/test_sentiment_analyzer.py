"""
Comprehensive tests for Sentiment Analysis Engine
Tests both Tier 1 and Tier 2 functionality

Author: Assignment Solution
Date: 2025
"""

import unittest
from sentiment_analyzer import SentimentAnalyzer, SentimentLabel


class TestSentimentAnalyzer(unittest.TestCase):
    """Test suite for sentiment analysis"""

    def setUp(self):
        """Initialize analyzer for each test"""
        self.analyzer = SentimentAnalyzer()

    def test_analyze_positive_statement(self):
        """Tier 2: Test positive sentiment detection"""
        result = self.analyzer.analyze_statement("I love this! It's wonderful!")
        self.assertEqual(result.label, SentimentLabel.POSITIVE.value)
        self.assertGreater(result.score, 0.5)
        self.assertGreater(result.confidence, 0)

    def test_analyze_negative_statement(self):
        """Tier 2: Test negative sentiment detection"""
        result = self.analyzer.analyze_statement("This is terrible and disappointing")
        self.assertEqual(result.label, SentimentLabel.NEGATIVE.value)
        self.assertLess(result.score, -0.5)

    def test_analyze_neutral_statement(self):
        """Tier 2: Test neutral sentiment detection"""
        result = self.analyzer.analyze_statement("The weather is cloudy today")
        self.assertEqual(result.label, SentimentLabel.NEUTRAL.value)

    def test_empty_statement_raises_error(self):
        """Tier 2: Test error handling for empty input"""
        with self.assertRaises(ValueError):
            self.analyzer.analyze_statement("")

    def test_statement_result_structure(self):
        """Tier 2: Test that statement result has all required fields"""
        result = self.analyzer.analyze_statement("Great job!")
        self.assertIsNotNone(result.text)
        self.assertIsNotNone(result.label)
        self.assertIsNotNone(result.score)
        self.assertIsNotNone(result.confidence)
        self.assertIsNotNone(result.vader_scores)

    def test_conversation_positive_sentiment(self):
        """Tier 1: Test conversation with positive sentiment"""
        messages = [
            {'role': 'user', 'content': 'I love your service!'},
            {'role': 'assistant', 'content': 'Thank you!'},
            {'role': 'user', 'content': 'It exceeded my expectations!'},
        ]
        analysis = self.analyzer.analyze_conversation(messages)
        self.assertEqual(analysis.overall_label, SentimentLabel.POSITIVE.value)
        self.assertGreater(analysis.positive_count, 0)

    def test_conversation_negative_sentiment(self):
        """Tier 1: Test conversation with negative sentiment"""
        messages = [
            {'role': 'user', 'content': 'Your service is terrible'},
            {'role': 'assistant', 'content': 'We apologize.'},
            {'role': 'user', 'content': 'This is unacceptable!'},
        ]
        analysis = self.analyzer.analyze_conversation(messages)
        self.assertEqual(analysis.overall_label, SentimentLabel.NEGATIVE.value)
        self.assertGreater(analysis.negative_count, 0)

    def test_conversation_mixed_sentiment(self):
        """Tier 1: Test conversation with mixed sentiments"""
        messages = [
            {'role': 'user', 'content': 'I like some features but hate others'},
            {'role': 'assistant', 'content': 'Tell me more'},
            {'role': 'user', 'content': 'Overall it is okay'},
        ]
        analysis = self.analyzer.analyze_conversation(messages)
        self.assertIsNotNone(analysis.overall_label)
        self.assertEqual(analysis.total_messages, 3)

    def test_conversation_statistics(self):
        """Tier 1: Test conversation statistics calculation"""
        messages = [
            {'role': 'user', 'content': 'Good'},
            {'role': 'assistant', 'content': 'Response'},
            {'role': 'user', 'content': 'Bad'},
        ]
        analysis = self.analyzer.analyze_conversation(messages)
        self.assertEqual(analysis.total_messages, 2)
        self.assertEqual(analysis.positive_count, 1)
        self.assertEqual(analysis.negative_count, 1)
        self.assertEqual(analysis.neutral_count, 0)

    def test_trend_improving(self):
        """Tier 2: Test trend detection - improving sentiment"""
        messages = [
            {'role': 'user', 'content': 'Terrible start'},
            {'role': 'assistant', 'content': 'Response'},
            {'role': 'user', 'content': 'Getting better'},
            {'role': 'user', 'content': 'Excellent now!'},
        ]
        analysis = self.analyzer.analyze_conversation(messages)
        self.assertIn("Improving", analysis.trend)

    def test_trend_declining(self):
        """Tier 2: Test trend detection - declining sentiment"""
        messages = [
            {'role': 'user', 'content': 'Great start!'},
            {'role': 'assistant', 'content': 'Response'},
            {'role': 'user', 'content': 'Getting worse'},
            {'role': 'user', 'content': 'Terrible now'},
        ]
        analysis = self.analyzer.analyze_conversation(messages)
        self.assertIn("Declining", analysis.trend)

    def test_emotional_progression(self):
        """Tier 2: Test emotional progression tracking"""
        messages = [
            {'role': 'user', 'content': 'Great!'},
            {'role': 'user', 'content': 'Fine.'},
            {'role': 'user', 'content': 'Terrible'},
        ]
        analysis = self.analyzer.analyze_conversation(messages)
        self.assertEqual(len(analysis.emotional_progression), 3)
        self.assertIn(SentimentLabel.POSITIVE.value, analysis.emotional_progression)
        self.assertIn(SentimentLabel.NEGATIVE.value, analysis.emotional_progression)

    def test_empty_conversation_raises_error(self):
        """Tier 1: Test error handling for empty conversation"""
        with self.assertRaises(ValueError):
            self.analyzer.analyze_conversation([])

    def test_conversation_no_user_messages_raises_error(self):
        """Tier 1: Test error handling when no user messages"""
        messages = [
            {'role': 'assistant', 'content': 'Response'},
        ]
        with self.assertRaises(ValueError):
            self.analyzer.analyze_conversation(messages)

    def test_to_dict_conversion(self):
        """Test JSON serialization of results"""
        result = self.analyzer.analyze_statement("Test")
        result_dict = result.to_dict()
        self.assertIsInstance(result_dict, dict)
        self.assertIn('label', result_dict)
        self.assertIn('score', result_dict)

    def test_confidence_range(self):
        """Tier 2: Test confidence scores are in valid range"""
        result = self.analyzer.analyze_statement("Some text")
        self.assertGreaterEqual(result.confidence, 0)
        self.assertLessEqual(result.confidence, 1)

    def test_multiple_statements_consistency(self):
        """Tier 2: Test consistency across multiple analyses"""
        text = "I really love this!"
        result1 = self.analyzer.analyze_statement(text)
        result2 = self.analyzer.analyze_statement(text)
        self.assertEqual(result1.label, result2.label)
        self.assertEqual(result1.score, result2.score)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios"""

    def setUp(self):
        """Initialize analyzer for each test"""
        self.analyzer = SentimentAnalyzer()

    def test_very_long_text(self):
        """Test analysis of very long text"""
        long_text = "Great! " * 100
        result = self.analyzer.analyze_statement(long_text)
        self.assertIsNotNone(result.label)

    def test_special_characters(self):
        """Test text with special characters"""
        text = "I'm so happy!!! @#$%^&*()"
        result = self.analyzer.analyze_statement(text)
        self.assertIsNotNone(result.label)

    def test_mixed_case_text(self):
        """Test text with mixed case"""
        text = "I LoVe ThIs!"
        result = self.analyzer.analyze_statement(text)
        self.assertIsNotNone(result.label)

    def test_numbers_in_text(self):
        """Test text with numbers"""
        text = "I gave it 5 stars! Amazing!"
        result = self.analyzer.analyze_statement(text)
        self.assertEqual(result.label, SentimentLabel.POSITIVE.value)


if __name__ == '__main__':
    unittest.main()
