# Chatbot with Sentiment Analysis(SentimentBot)

A production-grade, modular Python chatbot that conducts conversations and performs comprehensive sentiment analysis.

## Goal 

Most of the chatbots just reply, but they don’t understand emotions. They treat everything as just text, without really knowing if the user is happy, disappointed, stressed, or excited.

My chatbot is designed to fix that by performing sentiment analysis at two levels:

### Tier 1- Conversation-Level Analysis

* It keeps the full conversation history.
* At the end, it analyzes all user messages and reports:
* Overall sentiment from -1 (negative) to +1 (positive),
* How many messages were positive, negative, or neutral,
* And whether the mood improved, declined, or stayed stable.

### Tier 2- Statement-Level Analysis

* For every user message, it shows
* Sentiment label (positive / negative / neutral).
* A numeric score and confidence,
* Subjectivity and other components.

This allows tracking mood shifts across the chat. So you get both the big-picture mood and per-message analysis.


### Additional Enhancements
* **Modular Architecture**: Clean separation of concerns (chatbot, analyzer, interface)
* **Production-Grade Code**: Comprehensive error handling and logging
* **Full Test Suite**: 20+ unit tests covering both tiers
* **JSON Export**: Save sentiment analysis results for later analysis
* **Session Summaries**: Statistics about conversation duration and message counts
* **Subjectivity Scoring**: Measures how subjective user messages are
* **Interactive CLI**: User-friendly command-line interface with help

## Project Structure

SentimentBot/

│

├── chatbot.py

├── main.py

├── sentiment_analyzer.py

├── requirements.txt

├── README.md

├── package.json

│

├── tests/

│   ├── __init__.py

│   ├── test_chatbot.py

│   ├── test_sentiment_analyzer.py

│

└── __pycache__/

    ├── chatbot.cpython-314.pyc
    
    ├── sentiment_analyzer.cpython-314.pyc


## Installation

### Prerequisites
* Python 3.7 or higher
* pip (Python package manager)

### Setup

**1. Clone the repository:**
* git clone (repository-url)
* cd SentimentBot

**2. Install dependencies:**
* pip install -r requirements.txt

**3. Run Interactive Chatbot**
* python main.py


### Interactive Commands

Once the chatbot is running, you can:

* **Send messages**: Type any message to chat
* **View sentiment analysis**: Type `analysis` to see conversation-level sentiment (Tier 1) and Tier 2 enhancements
* **Toggle statement-level display**: Type `toggle` to show/hide individual message sentiments
* **Export results**: Type `export` to save sentiment analysis to JSON file
* **End conversation**: Type `quit` to end the session

### Example Session

**You: Hello! I'm excited about this chatbot!**

[Statement-Level Sentiment]

  Sentiment: Positive
  
  Score: 0.753
  
  Confidence: 85.21%
  

**Bot: Hi there! I'm ready to listen and help.**


**You: But I'm worried it won't work properly.**


[Statement-Level Sentiment]

  Sentiment: Negative
  
  Score: -0.420
  
  Confidence: 62.30%

**You: analysis**





           CONVERSATION-LEVEL ANALYSIS - TIER 1


Overall Sentiment: Positive

Overall Score: 0.167

Average Confidence: 73.76%

Message Breakdown:

  Total Messages: 2
  
  Positive: 1
  
  Negative: 1
  Neutral: 0
  
                 SENTIMENT-LEVEL ANALYSIS - TIER 2

  Stable - Sentiment remained consistent

Emotional Progression:

  Positive → Negative


## Module Overview

**1. sentiment_analyzer.py**

Main sentiment analysis engine with: 
* SentimentAnalyzer: Main analyzer class
* SentimentResult: Data class for individual message analysis (Tier 2)
* ConversationSentiment: Data class for conversation analysis (Tier 1)
* Dual-engine analysis using VADER and TextBlob
* Trend analysis function
#### Key Methods  
* analyze_statement(text) - Tier 2: Analyze single message.
* analyze_conversation(messages) - Tier 1: Analyze full conversation.
* export_results(analysis) - Export to JSON

**2. chatbot.py**

Conversation management and response generation:
* Chatbot: Main chatbot class
* Conversation history management
* Context-aware response generation
* Modular architecture for easy extensio
#### Key Methods  
* add_message(role, content) - Add to conversation
* get_history() - Retrieve full conversation
* generate_response(user_input) - Generate contextual response
* get_summary() - Get conversation statistics

**3. python main.py**

Interactive CLI interface:
* ChatbotInterface: Main user-facing interface
* Interactive command loop
* Statement and conversation sentiment display
* Export functionality

**4. tests/**

* Tests for analyzer, chatbot, and edge cases
* Covers positive/negative/neutral detection
* Tests trend detection & error handling

### Algorithm Details 
**Dual-Engine Approach:**

**VADER(Valence Aware Dictionary and sEntiment Reasoner)**
* Specialized for social media and informal text
* Provides compound score and component scores
* Good for understanding intensity

**TextBlob**
* Provides polarity (-1 to 1) and subjectivity (0 to 1)
* Complements VADER for comprehensive analysis
* Captures subjective language

**Classification Thresholds:**
* Positive: compound score ≥ 0.05
* Negative: compound score ≤ -0.05
* Neutral: -0.05 < compound score < 0.05

**Trend Detection:** 
* Splits conversation in half
*  Compares average sentiment of first half vs. second half
*  Threshold: 0.1 point difference for trend change
*  Categories: Improving, Declining, Stable

 ## Tech Stack

* **Python 3.7+**: Core language
* **NLTK**: VADER sentiment analysis
* **TextBlob**: Polarity and subjectivity analysis
* **unittest**: Comprehensive test framework
* **JSON**: Data export and serialization

