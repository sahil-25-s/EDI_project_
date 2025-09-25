from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# In-memory storage (resets on each deployment)
data_store = {"users": {}, "problems": {
    "1": {
        "title": "Two Sum",
        "difficulty": "Easy",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        "examples": [{"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]"}],
        "xp": 10
    },
    "2": {
        "title": "Reverse Integer",
        "difficulty": "Medium", 
        "description": "Given a signed 32-bit integer x, return x with its digits reversed.",
        "examples": [{"input": "x = 123", "output": "321"}],
        "xp": 20
    }
}}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/platform')
def platform():
    return render_template('platform.html')

@app.route('/api/user/<username>')
def get_user(username):
    if username not in data_store['users']:
        data_store['users'][username] = {
            "xp": 0,
            "level": 1,
            "streak": 0,
            "last_solved": None,
            "solved": [],
            "achievements": []
        }
    
    user = data_store['users'][username]
    user['level'] = user['xp'] // 100 + 1
    return jsonify(user)

@app.route('/api/problems')
def get_problems():
    return jsonify(data_store['problems'])

@app.route('/api/submit', methods=['POST'])
def submit_solution():
    username = request.json['username']
    problem_id = request.json['problem_id']
    
    problem = data_store['problems'][problem_id]
    
    if username not in data_store['users']:
        data_store['users'][username] = {"xp": 0, "level": 1, "streak": 0, "last_solved": None, "solved": [], "achievements": []}
    
    user = data_store['users'][username]
    if problem_id not in user['solved']:
        user['solved'].append(problem_id)
        user['xp'] += problem['xp']
        
        today = datetime.now().date()
        if user['last_solved']:
            last_date = datetime.fromisoformat(user['last_solved']).date()
            if today - last_date == timedelta(days=1):
                user['streak'] += 1
            elif today - last_date > timedelta(days=1):
                user['streak'] = 1
        else:
            user['streak'] = 1
        
        user['last_solved'] = today.isoformat()
    
    return jsonify({"success": True, "xp_gained": problem['xp'], "user": user})