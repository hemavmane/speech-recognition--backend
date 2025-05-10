from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  

SUBMISSIONS_DIR = 'submissions'


if not os.path.exists(SUBMISSIONS_DIR):
    os.makedirs(SUBMISSIONS_DIR)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Speech Recognition Backend is running!'}), 200

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        form_data = request.json

        
        if not all(key in form_data for key in ['name', 'email', 'message']):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

        form_data['timestamp'] = datetime.now().isoformat()

        
        filename = f"{form_data['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(SUBMISSIONS_DIR, filename)

        
        with open(filepath, 'w') as f:
            json.dump(form_data, f, indent=2)

        print(f"Form submitted: {form_data['name']} ({form_data['email']})")

        return jsonify({
            'status': 'success', 
            'message': 'Form submitted successfully'
        }), 200

    except Exception as e:
        print(f"Error processing form submission: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while processing your request'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
