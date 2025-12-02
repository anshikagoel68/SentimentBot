"""
Sentiment Analysis Engine
Tier 1 & Tier 2 Implementation

This module provides robust sentiment analysis using dual-engine approach:
- VADER: For social media and real-time text
- TextBlob: For polarity and subjectivity scoring

Author: Assignment Solution
Date: 2025
"""

from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from typing import Dict, List, Tuple
import json
from dataclasses import dataclass, asdict
from enum import Enum

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

try:
    nltk.data.find('punkt')
except LookupError:
    nltk.download('punkt')


class SentimentLabel(Enum):
    """Sentiment classification labels"""
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"


@dataclass
class SentimentResult:
    """Data class for individual sentiment analysis result"""
    text: str
    label: str
    score: float
    confidence: float
    vader_scores: Dict[str, float]
    textblob_polarity: float
    textblob_subjectivity: float

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class ConversationSentiment:
    """Data class for overall conversation sentiment analysis"""
    overall_label: str
    overall_score: float
    total_messages: int
    positive_count: int
    negative_count: int
    neutral_count: int
    average_confidence: float
    trend: str
    message_sentiments: List[Dict]
    emotional_progression: List[str]

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


class SentimentAnalyzer:
    """Production-grade sentiment analysis engine"""

    def __init__(self):
        """Initialize the sentiment analyzer with VADER and TextBlob"""
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.threshold_positive = 0.05
        self.threshold_negative = -0.05

    def analyze_statement(self, text: str) -> SentimentResult:
        """
        Analyze sentiment of a single statement (Tier 2 Feature)
        
        Args:
            text: The text to analyze
            
        Returns:
            SentimentResult object with detailed sentiment information
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        # VADER Analysis
        vader_scores = self.vader_analyzer.polarity_scores(text)
        
        # TextBlob Analysis
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        # Determine label based on VADER compound score
        compound = vader_scores['compound']
        
        if compound >= self.threshold_positive:
            label = SentimentLabel.POSITIVE.value
        elif compound <= self.threshold_negative:
            label = SentimentLabel.NEGATIVE.value
        else:
            label = SentimentLabel.NEUTRAL.value

        # Calculate confidence based on intensity
        confidence = abs(compound)
        
        return SentimentResult(
            text=text,
            label=label,
            score=compound,
            confidence=confidence,
            vader_scores=vader_scores,
            textblob_polarity=polarity,
            textblob_subjectivity=subjectivity
        )

    def analyze_conversation(self, messages: List[Dict]) -> ConversationSentiment:
        """
        Analyze sentiment for entire conversation (Tier 1 Feature)
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            
        Returns:
            ConversationSentiment object with conversation-level analysis
        """
        if not messages:
            raise ValueError("Messages list cannot be empty")

        user_messages = [
            msg for msg in messages if msg.get('role') == 'user'
        ]

        if not user_messages:
            raise ValueError("No user messages found in conversation")

        # Analyze each user message
        sentiments = []
        emotional_progression = []
        
        for msg in user_messages:
            content = msg.get('content', '').strip()
            if content:
                result = self.analyze_statement(content)
                sentiments.append(result)
                emotional_progression.append(result.label)

        # Calculate statistics
        positive_count = sum(1 for s in sentiments if s.label == SentimentLabel.POSITIVE.value)
        negative_count = sum(1 for s in sentiments if s.label == SentimentLabel.NEGATIVE.value)
        neutral_count = sum(1 for s in sentiments if s.label == SentimentLabel.NEUTRAL.value)

        # Calculate overall sentiment
        average_score = sum(s.score for s in sentiments) / len(sentiments)
        average_confidence = sum(s.confidence for s in sentiments) / len(sentiments)

        # Determine overall label
        if average_score >= self.threshold_positive:
            overall_label = SentimentLabel.POSITIVE.value
        elif average_score <= self.threshold_negative:
            overall_label = SentimentLabel.NEGATIVE.value
        else:
            overall_label = SentimentLabel.NEUTRAL.value

        # Determine trend (Tier 2 Enhancement)
        trend = self._analyze_trend(sentiments)

        # Convert sentiments to dictionaries
        message_sentiments = [s.to_dict() for s in sentiments]

        return ConversationSentiment(
            overall_label=overall_label,
            overall_score=average_score,
            total_messages=len(sentiments),
            positive_count=positive_count,
            negative_count=negative_count,
            neutral_count=neutral_count,
            average_confidence=average_confidence,
            trend=trend,
            message_sentiments=message_sentiments,
            emotional_progression=emotional_progression
        )

    def _analyze_trend(self, sentiments: List[SentimentResult]) -> str:
        """
        Analyze the trend in sentiment across messages
        
        Args:
            sentiments: List of SentimentResult objects
            
        Returns:
            Trend description (Improving, Declining, or Stable)
        """
        if len(sentiments) < 2:
            return "Insufficient data for trend analysis"

        # Split conversation in half
        midpoint = len(sentiments) // 2
        first_half_score = sum(s.score for s in sentiments[:midpoint]) / len(sentiments[:midpoint])
        second_half_score = sum(s.score for s in sentiments[midpoint:]) / len(sentiments[midpoint:])

        difference = second_half_score - first_half_score
        threshold = 0.1

        if difference > threshold:
            return "Improving - Sentiment became more positive"
        elif difference < -threshold:
            return "Declining - Sentiment became more negative"
        else:
            return "Stable - Sentiment remained consistent"


def export_results(sentiment_analysis: ConversationSentiment, filename: str = "sentiment_analysis.json"):
    """Export sentiment analysis results to JSON file"""
    with open(filename, 'w') as f:
        json.dump(sentiment_analysis.to_dict(), f, indent=2)
    print(f"Results exported to {filename}")
