# Chatbot with Sentiment Analysis (SentimentBot)

This project features a production-grade, modular Python chatbot that not only responds intelligently but also understands user emotions through comprehensive, multi-layer sentiment analysis. Unlike traditional chatbots that treat all text the same, this system evaluates how the user feels throughout the conversation.

To achieve this, the chatbot performs sentiment analysis at two levels:

### Level 1- Conversation-Level Analysis

At the macro level, the chatbot analyzes the entire conversation history to:

* Compute an overall sentiment score (from -1 to +1)
* Count positive, negative, and neutral messages
* Detect emotional trends (improving, declining, or stable)

This provides a complete picture of the user’s emotional journey.

### Level 2- Statement-Level Analysis

At the micro level, each individual message is assessed for:

* Sentiment label (positive / negative / neutral)
* Polarity score and confidence
* Subjectivity and other linguistic features

This enables fine-grained tracking of how the user’s mood shifts message by message.

**Together, these two layers allow the chatbot to understand not just what the user says—but how they feel—resulting in a more emotionally aware conversational experience.**

## Features

* **Multi-layer Sentiment Analysis:** Uses both VADER and TextBlob for precise emotional understanding.
* **Conversation-Level Insights:** Aggregates overall sentiment, message distribution, and mood trends.
* **Statement-Level Insights:** Per-message polarity, subjectivity, sentiment label, and confidence.
* **Modular Architecture:** Clean separation of sentiment logic, chatbot logic, and user interface.
* **Conversation History Tracking:** Stores all messages along with metadata and sentiment metrics.
* **JSON Export:** Saves full chat sessions with all sentiment analysis results.
* **Production-Ready Structure:** Well-organized, testable, and extensible design.

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

## Module Overview

**1. sentiment_analyzer.py**

Main sentiment analysis engine with: 
* SentimentAnalyzer: Main analyzer class
* SentimentResult: Data class for individual message analysis (Tier 2)
* ConversationSentiment: Data class for conversation analysis (Tier 1)
* Dual-engine analysis using VADER and TextBlob
* Trend analysis function

**2. chatbot.py**

Conversation management and response generation:
* Chatbot: Main chatbot class
* Conversation history management
* Stores message metadata and stats
* Calls the sentiment analyzer for each message
  
**3. python main.py**

Interactive CLI interface:
* ChatbotInterface: Main user-facing interface
* Interactive command loop
* Statement and conversation sentiment display
* Export functionality

**4. tests**

* Tests for analyzer, chatbot, and edge cases
* Covers positive/negative/neutral detection
* Tests trend detection & error handling

## Algorithm Details 
**Dual-Engine Approach:**

**VADER(Valence Aware Dictionary and sEntiment Reasoner)**
* Specialized for social media, emojis and informal text
* Provides compound score and component scores
* Good for understanding intensity

**TextBlob**
* Provides polarity (-1 to 1) and subjectivity (0 to 1), better on formal/longer text.
* Complements VADER for comprehensive analysis
* Captures subjective language

### Classification Thresholds
* Positive: compound score ≥ 0.05
* Negative: compound score ≤ -0.05
* Neutral: -0.05 < compound score < 0.05

### Trend Detection
* Splits conversation in half
*  Compares average sentiment of first half vs. second half
*  Threshold: 0.1 point difference for trend change
*  Categories: Improving, Declining, Stable


## Installation & Setup

**1. Clone the repository:**
* git clone https://github.com/yourusername/sentimentbot.git
* cd sentimentbot
  
**2. Create a Virtual Environment:**
* python -m venv venv
* source venv/bin/activate        # Linux/macOS
* venv\Scripts\activate           # Windows

**3. Install dependencies:**
* pip install -r requirements.txt

**4. Download NLTK Data (VADER) and TextBlob**

**5. Run the chatbot**
* python main.py


## Interactive Commands

Once the chatbot is running, you can:

* **Send messages**: Type any message to chat
* **View sentiment analysis**: Type `analysis` to see conversation-level sentiment (Tier 1) and Tier 2 enhancements
* **Toggle statement-level display**: Type `toggle` to show/hide individual message sentiments
* **Export results**: Type `export` to save sentiment analysis to JSON file
* **End conversation**: Type `quit` to end the session

### Example Session

**You: Hello! I'm excited about this chatbot!**

[TIER 2: Statement-Level Sentiment Analysis]

  Sentiment: Positive
  
  Score: 0.753
  
  Confidence: 85.21%
  

**Bot: Hi there! I'm ready to listen and help.**


**You: But I'm worried it won't work properly.**

[TIER 2: Statement-Level Sentiment Analysis]

  Sentiment: Negative
  
  Score: -0.420
  
  Confidence: 62.30%

**You: analysis**

TIER 1: Conversation-Level Sentiment Analysis

Overall Sentiment: Positive

Overall Score: 0.167

Average Confidence: 73.76%

Message Breakdown:

Total Messages: 2
  
Positive: 1
  
Negative: 1
  
Neutral: 0
  
Final Output:

Overall conversation sentiment: Neutral – balanced or mixed sentiment

Sentiment Trend:

Improving - Sentiment became more positive

Emotional Progression:

Negative → Positive   
  
 ## Tech Stack

* **Python 3.7+**: Core language
* **NLTK**: VADER sentiment analysis
* **TextBlob**: Polarity and subjectivity analysis
* **unittest**: Comprehensive test framework
* **JSON**: Data export and serialization






