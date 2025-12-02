"""
Main Entry Point - Interactive Chatbot with Sentiment Analysis
Tier 1 & Tier 2 Implementation

This is the primary interface for the chatbot application.
Supports both Tier 1 (conversation-level) and Tier 2 (statement-level) sentiment analysis.

Author: Assignment Solution
Date: 2025
"""

from chatbot import Chatbot
from sentiment_analyzer import SentimentAnalyzer, export_results
import sys


class ChatbotInterface:
    """Main interface for interactive chatbot session"""

    def __init__(self):
        """Initialize chatbot and sentiment analyzer"""
        self.chatbot = Chatbot(name="SentimentBot")
        self.analyzer = SentimentAnalyzer()
        self.show_statement_sentiment = True  # Tier 2 feature toggle

    def display_welcome(self):
        """Display welcome message and instructions"""
        print("\n" + "="*70)
        print("INTERACTIVE CHATBOT WITH SENTIMENT ANALYSIS".center(70))
        print("="*70)
        print("\nTier 1 Implementation: Conversation-level sentiment analysis")
        print("Tier 2 Implementation: Statement-level sentiment analysis\n")
        print("Commands:")
        print("  - Type your message to chat")
        print("  - Type 'quit' to end conversation")
        print("  - Type 'analysis' to see current sentiment analysis")
        print("  - Type 'toggle' to toggle statement-level display")
        print("  - Type 'export' to save analysis to JSON file")
        print("\n" + "="*70 + "\n")

    def display_statement_sentiment(self, text: str):
        """
        Display statement-level sentiment analysis (Tier 2)
        
        Args:
            text: The statement to analyze
        """
        try:
            result = self.analyzer.analyze_statement(text)
            print(f"\n[Statement-Level Sentiment - Tier 2]")
            print(f"  Sentiment: {result.label}")
            print(f"  Confidence: {result.confidence:.2%}")
            print(f"  Score: {result.score:.3f}")
            print(f"  Subjectivity: {result.textblob_subjectivity:.2%}\n")
        except ValueError as e:
            print(f"\nError analyzing statement: {e}\n")

    def display_conversation_sentiment(self):
        """
        Display conversation-level sentiment analysis (Tier 1)
        """
        try:
            history = self.chatbot.get_history()
            if not history:
                print("\nNo conversation data to analyze yet.\n")
                return

            analysis = self.analyzer.analyze_conversation(history)

            print("\n" + "="*70)
            print("CONVERSATION-LEVEL SENTIMENT ANALYSIS - TIER 1".center(70))
            print("="*70)
            print(f"\nOverall Sentiment: {analysis.overall_label}")
            print(f"Overall Score: {analysis.overall_score:.3f}")
            print(f"Average Confidence: {analysis.average_confidence:.2%}")
            print(f"\nMessage Breakdown:")
            print(f"  Total Messages: {analysis.total_messages}")
            print(f"  Positive: {analysis.positive_count}")
            print(f"  Negative: {analysis.negative_count}")
            print(f"  Neutral: {analysis.neutral_count}")
            print(f"\nSentiment Trend (Tier 2 Enhancement):")
            print(f"  {analysis.trend}")
            print(f"\nEmotional Progression:")
            print(f"  {' → '.join(analysis.emotional_progression)}")
            print("\n" + "="*70 + "\n")

            return analysis

        except ValueError as e:
            print(f"\nError analyzing conversation: {e}\n")
            return None

    def run(self):
        """Run the interactive chatbot session"""
        self.display_welcome()

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                # Handle commands
                if user_input.lower() == 'quit':
                    print("\nEnding conversation...")
                    break

                elif user_input.lower() == 'analysis':
                    self.display_conversation_sentiment()
                    continue

                elif user_input.lower() == 'toggle':
                    self.show_statement_sentiment = not self.show_statement_sentiment
                    status = "enabled" if self.show_statement_sentiment else "disabled"
                    print(f"\nStatement-level sentiment display {status}.\n")
                    continue

                elif user_input.lower() == 'export':
                    try:
                        history = self.chatbot.get_history()
                        if history:
                            analysis = self.analyzer.analyze_conversation(history)
                            export_results(analysis)
                            print()
                        else:
                            print("\nNo conversation to export.\n")
                    except Exception as e:
                        print(f"\nError exporting results: {e}\n")
                    continue

                # Regular conversation flow
                self.chatbot.add_message('user', user_input)

                # Display statement-level sentiment if enabled (Tier 2)
                if self.show_statement_sentiment:
                    self.display_statement_sentiment(user_input)

                # Generate and display chatbot response
                response = self.chatbot.generate_response(user_input)
                self.chatbot.add_message('assistant', response)
                print(f"\nBot: {response}\n")

            except KeyboardInterrupt:
                print("\n\nChat interrupted by user.")
                break
            except Exception as e:
                print(f"\nError during chat: {e}\n")
                continue

        # Final sentiment analysis and summary
        print("\n" + "="*70)
        print("SESSION SUMMARY".center(70))
        print("="*70)

        summary = self.chatbot.get_summary()
        print(f"\nConversation Duration: {summary['duration']}")
        print(f"Total Exchanges: {summary['user_messages']}")

        # Display final conversation sentiment analysis
        self.display_conversation_sentiment()

        print("Thank you for using SentimentBot!")


def main():
    """Main entry point"""
    interface = ChatbotInterface()
    interface.run()


if __name__ == "__main__":
    main()
