from flask import Flask, render_template, request, jsonify
from actions import NLPChatbot

app = Flask(__name__)
chatbot = NLPChatbot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'response': 'Please say something!'})
    
    response = chatbot.process_input(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)