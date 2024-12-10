import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime
import json
import random
import re
from chat_log import ChatLogger

class NLPChatbot:
    def __init__(self):
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('vader_lexicon')
        
        self.sia = SentimentIntensityAnalyzer()
        self.conversation_history = []
        self.logger = ChatLogger()
        
        # Knowledge base
        self.knowledge_base = {
            "greetings": {
                "patterns": ["hello", "hi", "hey", "good morning", "good evening", "hi there"],
                "responses": [
                    "Hello! How can I help you today?",
                    "Hi there! What would you like to talk about?",
                    "Hey! I'm here to help. What's on your mind?"
                ]
            },
            "farewells": {
                "patterns": ["bye", "goodbye", "see you", "take care"],
                "responses": [
                    "Goodbye! Have a great day!",
                    "Bye! Feel free to come back anytime!",
                    "Take care! Looking forward to our next chat!"
                ]
            },
            "thanks": {
                "patterns": ["thank you", "thanks", "appreciate it"],
                "responses": [
                    "You're welcome!",
                    "Happy to help!",
                    "My pleasure!"
                ]
            },
            "capabilities": {
                "patterns": ["what can you do", "help me", "your capabilities", "what do you do"],
                "responses": [
                    """I can help you with:
1. General conversation and questions
2. Understanding your sentiment
3. Processing natural language
4. Learning from our interactions
5. Providing relevant information

Feel free to ask me anything!"""
                ]
            }
        }
        
        # Topic patterns
        self.topic_patterns = {
            "general_query": r"(?:what|how|why|when|where|who|tell me about|explain)",
            "opinion": r"(?:think|believe|feel|opinion|view)",
            "comparison": r"(?:compare|difference|better|worse|versus|vs)",
            "definition": r"(?:define|meaning of|what is|what are)",
            "example": r"(?:example|instance|show me|demonstrate)",
            "help": r"(?:help|assist|support|guide)"
        }

    def process_input(self, user_input):
        try:
            # Clean and normalize input
            cleaned_input = user_input.strip().lower()
            
            # Log the conversation
            self.conversation_history.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_input": user_input,
                "type": "user"
            })
            
            # Check for empty input
            if not cleaned_input:
                return "Please say something so I can help you!"
            
            # Check for greetings, farewells, and thanks
            for intent, data in self.knowledge_base.items():
                if any(pattern in cleaned_input for pattern in data["patterns"]):
                    response = random.choice(data["responses"])
                    self.log_interaction(user_input, response, intent)
                    return response
            
            # Process the input using NLP
            response = self.generate_response(cleaned_input)
            self.log_interaction(user_input, response, "conversation")
            return response

        except Exception as e:
            print(f"Error: {str(e)}")
            return "I apologize, but I encountered an error. Could you please rephrase that?"

    def generate_response(self, text):
        # Tokenize and analyze the input
        tokens = word_tokenize(text)
        pos_tags = nltk.pos_tag(tokens)
        
        # Analyze sentiment
        sentiment = self.analyze_sentiment(text)
        
        # Identify topic and intent
        topic = self.identify_topic(text)
        
        # Generate appropriate response based on analysis
        if sentiment['compound'] < -0.3:
            response = self.handle_negative_sentiment(text)
        elif sentiment['compound'] > 0.3:
            response = self.handle_positive_sentiment(text)
        else:
            response = self.generate_neutral_response(text, topic)

        return response

    def analyze_sentiment(self, text):
        return self.sia.polarity_scores(text)

    def identify_topic(self, text):
        for topic, pattern in self.topic_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                return topic
        return "general"

    def handle_negative_sentiment(self, text):
        responses = [
            "I sense some concern in your message. How can I help?",
            "Let's work through this together. What specific help do you need?",
            "I understand your frustration. Could you tell me more about it?"
        ]
        return random.choice(responses)

    def handle_positive_sentiment(self, text):
        responses = [
            "I'm glad you're feeling positive! What would you like to explore?",
            "That's great! How can I help you further?",
            "Wonderful! What else would you like to know?"
        ]
        return random.choice(responses)

    def generate_neutral_response(self, text, topic):
        if topic == "general_query":
            return self.handle_general_query(text)
        elif topic == "definition":
            return self.handle_definition_request(text)
        elif topic == "example":
            return self.handle_example_request(text)
        else:
            return "I understand you're asking about something. Could you be more specific?"

    def handle_general_query(self, text):
        # Extract key nouns from the query
        tokens = word_tokenize(text)
        pos_tags = nltk.pos_tag(tokens)
        nouns = [word for word, pos in pos_tags if pos.startswith('NN')]
        
        if nouns:
            return f"I see you're asking about {', '.join(nouns)}. Could you be more specific about what you'd like to know?"
        return "What specific information would you like to know?"

    def handle_definition_request(self, text):
        tokens = word_tokenize(text)
        pos_tags = nltk.pos_tag(tokens)
        nouns = [word for word, pos in pos_tags if pos.startswith('NN')]
        
        if nouns:
            return f"You're asking for a definition of {nouns[-1]}. Could you provide more context about what aspect you'd like to understand?"
        return "What term would you like me to define?"

    def handle_example_request(self, text):
        return "I understand you're looking for an example. Could you specify the topic or concept you'd like an example of?"

    def log_interaction(self, user_input, response, interaction_type):
        self.logger.log_conversation(
            user_input=user_input,
            bot_response=response,
            question_type=interaction_type
        )

def main():
    chatbot = NLPChatbot()
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    NLP Chatbot Assistant                      ║
╚══════════════════════════════════════════════════════��═══════╝

Welcome! I'm your AI chatbot powered by Natural Language Processing.
I can understand and respond to your messages in a natural way.

Type 'help' to see what I can do, or 'quit' to exit.
""")
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() == 'help':
                print("""
🤖 I can help you with:
• General conversations and questions
• Understanding your sentiments
• Providing relevant information
• Learning from our interactions
• Natural language processing

Just type naturally, and I'll do my best to understand and respond!
""")
                continue
                
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n🤖 Goodbye! Have a great day! 👋")
                break
            
            response = chatbot.process_input(user_input)
            print("\n🤖 Bot:", response)
            
        except KeyboardInterrupt:
            print("\n\n🤖 Goodbye! Have a great day! 👋")
            break
        except Exception as e:
            print("\n⚠️ Something went wrong. Please try again.")
            continue

if __name__ == "__main__":
    main()
