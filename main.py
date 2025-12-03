
from chatbot import Chatbot
from sentiment_analyzer import SentimentAnalyzer, export_results


class ChatbotInterface:
    """Main interface for interactive chatbot session"""

    def __init__(self):
        self.chatbot = Chatbot(name="SentimentBot")
        self.analyzer = SentimentAnalyzer()
        self.show_statement_sentiment = True  # Tier 2 enabled by default

    def display_welcome(self):
        print("\n===========================================================")
        print(        "INTERACTIVE CHATBOT WITH SENTIMENT ANALYSIS"    )
        print("===========================================================\n")
        print("Tier 1: Conversation-Level Sentiment (Required)")
        print("Tier 2: Statement-Level Sentiment (Optional but Included)\n")
        print("Commands:")
        print("  - Enter message to chat")
        print("  - 'analysis'  → view conversation-level sentiment")
        print("  - 'toggle'    → enable/disable Tier 2 statement sentiment")
        print("  - 'export'    → save sentiment analysis to JSON")
        print("  - 'quit'      → exit chatbot")
        print("\n===========================================================\n")

   
    # TIER 2: STATEMENT LEVEL ANALYSIS

    def display_statement_sentiment(self, text: str):
        """Tier 2: Statement-level sentiment analysis"""
        try:
            result = self.analyzer.analyze_statement(text)
            print("\n[TIER 2: Statement-Level Sentiment Analysis]")
            print(f"  Sentiment:     {result.label}")
            print(f"  Score:         {result.score:+.3f}")
            print(f"  Confidence:    {result.confidence:.2%}")
            print(f"  Subjectivity:  {result.textblob_subjectivity:.2%}\n")
        except ValueError as e:
            print(f"\nError analyzing statement: {e}\n")
  
    # TIER 1: CONVERSATION LEVEL ANALYSIS
    
    def display_conversation_sentiment(self):
        """Tier 1: Conversation-level sentiment analysis"""
        try:
            history = self.chatbot.get_history()
            if not history:
                print("\nNo messages yet to analyze.\n")
                return

            analysis = self.analyzer.analyze_conversation(history)

            
            print("\n[TIER 1: Conversation-Level Sentiment Analysis]\n")

            print(f"Overall Sentiment: {analysis.overall_label}")
            print(f"Overall Score:     {analysis.overall_score:.3f}")
            print(f"Avg Confidence:    {analysis.average_confidence:.2%}")

            print("\nMessage Breakdown:")
            print(f"  Total:    {analysis.total_messages}")
            print(f"  Positive: {analysis.positive_count}")
            print(f"  Negative: {analysis.negative_count}")
            print(f"  Neutral:  {analysis.neutral_count}")

            interpretation = {
                "Positive": "overall positivity",
                "Negative": "general dissatisfaction",
                "Neutral": "balanced or mixed sentiment"
            }

            print("\nFinal Output:")
            print(f"Overall conversation sentiment: {analysis.overall_label} – {interpretation.get(analysis.overall_label, '')}")

            print("\nSentiment Trend:")
            print(f"  {analysis.trend}")

            print("\nEmotional Progression:")
            print("  " + " → ".join(analysis.emotional_progression))

            print()

        except ValueError as e:
            print(f"\nError analyzing conversation: {e}\n")

    # MAIN LOOP
  
    def run(self):
        self.display_welcome()

        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue

                cmd = user_input.lower()

                # Commands
                if cmd == "quit":
                    print("\nEnding conversation...")
                    break

                if cmd == "analysis":
                    self.display_conversation_sentiment()
                    continue

                if cmd == "toggle":
                    self.show_statement_sentiment = not self.show_statement_sentiment
                    state = "ENABLED" if self.show_statement_sentiment else "DISABLED"
                    print(f"\nTier 2 statement-level sentiment is now {state}.\n")
                    continue

                if cmd == "export":
                    history = self.chatbot.get_history()
                    if history:
                        analysis = self.analyzer.analyze_conversation(history)
                        export_results(analysis)
                        print("\nExport completed.\n")
                    else:
                        print("\nNo conversation to export.\n")
                    continue

                # Add user message
                self.chatbot.add_message("user", user_input)

                # Tier 2 output
                if self.show_statement_sentiment:
                    self.display_statement_sentiment(user_input)

                # Bot response
                response = self.chatbot.generate_response(user_input)
                self.chatbot.add_message("assistant", response)
                print(f"\nBot: {response}\n")

            except KeyboardInterrupt:
                print("\nConversation interrupted.")
                break

            except Exception as e:
                print(f"\nError: {e}\n")

        # End of session summary
       
        print("SESSION SUMMARY")
       
        summary = self.chatbot.get_summary()
        print(f"Duration:        {summary['duration']}")
        print(f"User Messages:   {summary['user_messages']}")

       
        self.display_conversation_sentiment()

        print("Thank you for using SentimentBot!")


def main():
    ChatbotInterface().run()


if __name__ == "__main__":
    main()
