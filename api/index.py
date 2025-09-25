from flask import Flask, jsonify, request
from datetime import datetime, timedelta

app = Flask(__name__)

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
    return '''<!DOCTYPE html>
<html><head><title>CodeQuest</title></head>
<body>
<h1>🎮 CodeQuest</h1>
<p>Level Up Your Coding Skills</p>
<a href="/platform">Start Coding</a>
</body></html>'''

@app.route('/platform')
def platform():
    return '''<!DOCTYPE html>
<html><head><title>CodeQuest Platform</title></head>
<body>
<h1>🎮 CodeQuest Platform</h1>
<input type="text" id="username" placeholder="Enter username">
<div id="problems"></div>
<script>
fetch('/api/problems').then(r=>r.json()).then(data=>{
    document.getElementById('problems').innerHTML = Object.entries(data).map(([id,p])=>
        `<div><h3>${p.title}</h3><p>${p.description}</p><button onclick="solve('${id}')">Solve</button></div>`
    ).join('');
});
function solve(id){alert('Problem '+id+' selected!');}
</script>
</body></html>'''

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
    data = request.get_json()
    username = data['username']
    problem_id = data['problem_id']
    
    problem = data_store['problems'][problem_id]
    
    if username not in data_store['users']:
        data_store['users'][username] = {"xp": 0, "level": 1, "streak": 0, "last_solved": None, "solved": [], "achievements": []}
    
    user = data_store['users'][username]
    if problem_id not in user['solved']:
        user['solved'].append(problem_id)
        user['xp'] += problem['xp']
        user['last_solved'] = datetime.now().date().isoformat()
    
    return jsonify({"success": True, "xp_gained": problem['xp'], "user": user})