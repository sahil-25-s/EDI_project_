from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Load problems and user data
def load_data():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            return json.load(f)
    return {"users": {}, "problems": get_default_problems()}

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=2)

def get_default_problems():
    return {
        "1": {
            "title": "Two Sum",
            "difficulty": "Easy",
            "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "examples": [{"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]"}],
            "xp": 10,
            "test_cases": [
                {"input": "[2,7,11,15]\n9", "output": "[0, 1]"},
                {"input": "[3,2,4]\n6", "output": "[1, 2]"}
            ]
        },
        "2": {
            "title": "Reverse Integer",
            "difficulty": "Medium", 
            "description": "Given a signed 32-bit integer x, return x with its digits reversed.",
            "examples": [{"input": "x = 123", "output": "321"}],
            "xp": 20,
            "test_cases": [
                {"input": "123", "output": "321"},
                {"input": "-123", "output": "-321"}
            ]
        }
    }

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/platform')
def platform():
    return render_template('platform.html')

@app.route('/api/user/<username>')
def get_user(username):
    data = load_data()
    if username not in data['users']:
        data['users'][username] = {
            "xp": 0,
            "level": 1,
            "streak": 0,
            "last_solved": None,
            "solved": [],
            "achievements": []
        }
        save_data(data)
    
    user = data['users'][username]
    user['level'] = user['xp'] // 100 + 1
    return jsonify(user)

@app.route('/api/problems')
def get_problems():
    data = load_data()
    return jsonify(data['problems'])

@app.route('/api/submit', methods=['POST'])
def submit_solution():
    username = request.json['username']
    problem_id = request.json['problem_id']
    code = request.json['code']
    
    data = load_data()
    problem = data['problems'][problem_id]
    
    # Simplified test (code execution removed for Vercel)
    passed = True  # In production, implement proper testing
    
    if passed:
        if username not in data['users']:
            data['users'][username] = {"xp": 0, "level": 1, "streak": 0, "last_solved": None, "solved": [], "achievements": []}
        
        user = data['users'][username]
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
            check_achievements(user)
        
        save_data(data)
        return jsonify({"success": True, "xp_gained": problem['xp'], "user": user})
    
    return jsonify({"success": False, "error": "Tests failed"})

def check_achievements(user):
    achievements = []
    if user['xp'] >= 100 and "First Century" not in user['achievements']:
        achievements.append("First Century")
    if user['streak'] >= 7 and "Week Warrior" not in user['achievements']:
        achievements.append("Week Warrior")
    if len(user['solved']) >= 10 and "Problem Solver" not in user['achievements']:
        achievements.append("Problem Solver")
    
    user['achievements'].extend(achievements)
    return achievements

# Vercel handler
if __name__ == '__main__':
    app.run(debug=True)