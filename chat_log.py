import csv
from datetime import datetime

class ChatLogger:
    def __init__(self, filename='chat_log.csv'):
        self.filename = filename
        self.setup_log_file()
    
    def setup_log_file(self):
        with open(self.filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # If file is empty
                writer.writerow(['Timestamp', 'User Input', 'Bot Response', 'Question Type', 'Career Field'])
    
    def log_conversation(self, user_input, bot_response, question_type=None, career_field=None):
        with open(self.filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                user_input,
                bot_response,
                question_type or 'general',
                career_field or 'none'
            ]) 