from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
import os
from datetime import datetime, timedelta
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/exam_practice_db"
app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
mongo = PyMongo(app)

# OpenAI configuration
openai.api_key = os.environ.get('OPENAI_API_KEY')

# JWT token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = mongo.db.users.find_one({'_id': ObjectId(data['user_id'])})
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# User registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    new_user = {
        'username': data['username'],
        'password': hashed_password,
        'progress': {}
    }
    try:
        mongo.db.users.insert_one(new_user)
        return jsonify({'message': 'User registered successfully'}), 201
    except:
        return jsonify({'message': 'Error registering user'}), 500

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({'username': data['username']})
    if user and check_password_hash(user['password'], data['password']):
        token = jwt.encode({
            'user_id': str(user['_id']),
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

# Generate a question using GPT API
def generate_question(exam_type):
    prompt = f"Generate a multiple-choice question for {exam_type} exam. \n" \
             f"Format: Question: [question text]\n" \
             f"Options: [option1], [option2], [option3], [option4]\n" \
             f"Correct Answer(s): [index of correct option(s), zero-based]"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150
    )

    question_text, options, correct_answers = response.choices[0].text.strip().split('\n')
    
    return {
        'exam_type': exam_type,
        'question_text': question_text.replace('Question: ', ''),
        'options': options.replace('Options: ', '').split(', '),
        'correct_answers': eval(correct_answers.replace('Correct Answer(s): ', ''))
    }

# Get a question
@app.route('/question/<exam_type>', methods=['GET'])
@token_required
def get_question(current_user, exam_type):
    try:
        question = generate_question(exam_type)
        question_id = mongo.db.questions.insert_one(question).inserted_id
        question['_id'] = str(question_id)
        return jsonify(question)
    except Exception as e:
        return jsonify({'message': f'Error generating question: {str(e)}'}), 500

# Check answer
@app.route('/check-answer', methods=['POST'])
@token_required
def check_answer(current_user):
    data = request.get_json()
    try:
        question = mongo.db.questions.find_one({'_id': ObjectId(data['question_id'])})
        is_correct = sorted(data['user_answer']) == sorted(question['correct_answers'])

        # Update user progress
        exam_progress = current_user.get('progress', {}).get(question['exam_type'], {'correct': 0, 'total': 0})
        exam_progress['total'] += 1
        if is_correct:
            exam_progress['correct'] += 1
        
        mongo.db.users.update_one(
            {'_id': current_user['_id']},
            {'$set': {f'progress.{question["exam_type"]}': exam_progress}}
        )

        return jsonify({
            'is_correct': is_correct,
            'correct_answer': question['correct_answers'],
            'progress': exam_progress
        })
    except Exception as e:
        return jsonify({'message': f'Error checking answer: {str(e)}'}), 500

# Get user progress
@app.route('/progress', methods=['GET'])
@token_required
def get_progress(current_user):
    try:
        return jsonify(current_user.get('progress', {}))
    except Exception as e:
        return jsonify({'message': f'Error fetching progress: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)