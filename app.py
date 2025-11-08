from flask import Flask, request, jsonify, render_template
from query_agent import query_knowledge_base
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({'error': 'Question is required'}), 400

        question = data['question'].strip()
        if not question:
            return jsonify({'error': 'Question cannot be empty'}), 400

        logger.info(f"Processing question: {question}")
        answer = query_knowledge_base(question)

        return jsonify({'answer': answer})

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
