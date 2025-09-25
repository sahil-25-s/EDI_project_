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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeQuest - Level Up Your Coding Skills</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 2rem; }
        .hero-section { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: white; position: relative; overflow: hidden; }
        .navbar { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 2rem; position: relative; z-index: 10; }
        .nav-brand { font-size: 1.8rem; font-weight: bold; }
        .nav-links { display: flex; align-items: center; gap: 2rem; }
        .nav-link { color: white; text-decoration: none; transition: opacity 0.3s ease; }
        .nav-link:hover { opacity: 0.8; }
        .btn-cta { background: rgba(255, 255, 255, 0.2); color: white; padding: 0.75rem 1.5rem; border-radius: 25px; text-decoration: none; transition: all 0.3s ease; backdrop-filter: blur(10px); }
        .btn-cta:hover { background: rgba(255, 255, 255, 0.3); transform: translateY(-2px); }
        .hero-content { text-align: center; padding: 4rem 2rem; position: relative; z-index: 10; }
        .hero-title { font-size: 3.5rem; font-weight: bold; margin-bottom: 1.5rem; line-height: 1.2; }
        .highlight { background: linear-gradient(45deg, #ff6b35, #f7931e); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
        .hero-subtitle { font-size: 1.3rem; margin-bottom: 2.5rem; opacity: 0.9; max-width: 600px; margin-left: auto; margin-right: auto; }
        .hero-buttons { display: flex; gap: 1rem; justify-content: center; margin-bottom: 4rem; }
        .btn-primary { background: linear-gradient(45deg, #ff6b35, #f7931e); color: white; padding: 1rem 2rem; border-radius: 30px; text-decoration: none; font-weight: bold; transition: all 0.3s ease; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4); }
        .btn-primary:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(255, 107, 53, 0.6); }
        .hero-stats { display: flex; justify-content: center; gap: 4rem; margin-top: 3rem; }
        .stat { text-align: center; }
        .stat-number { font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem; }
        .stat-label { opacity: 0.8; font-size: 1rem; }
        .features-section { padding: 6rem 0; background: #f8f9fa; }
        .section-title { text-align: center; font-size: 2.5rem; margin-bottom: 3rem; color: #333; }
        .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-top: 3rem; }
        .feature-card { background: white; padding: 2rem; border-radius: 15px; text-align: center; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1); transition: transform 0.3s ease; }
        .feature-card:hover { transform: translateY(-5px); }
        .feature-icon { font-size: 3rem; margin-bottom: 1rem; }
        .feature-card h3 { font-size: 1.5rem; margin-bottom: 1rem; color: #667eea; }
        .feature-card p { color: #666; line-height: 1.6; }
        @media (max-width: 768px) { .hero-title { font-size: 2.5rem; } .hero-buttons { flex-direction: column; align-items: center; } .hero-stats { flex-direction: column; gap: 2rem; } }
    </style>
</head>
<body>
    <div class="hero-section">
        <nav class="navbar">
            <div class="nav-brand">🎮 CodeQuest</div>
            <div class="nav-links">
                <a href="#features" class="nav-link">Features</a>
                <a href="/platform" class="btn-cta">Start Coding</a>
            </div>
        </nav>
        <div class="hero-content">
            <h1 class="hero-title">Level Up Your <span class="highlight">Coding Skills</span></h1>
            <p class="hero-subtitle">Master Data Structures & Algorithms through gamified challenges. Earn XP, unlock achievements, and become a coding champion!</p>
            <div class="hero-buttons">
                <a href="/platform" class="btn-primary">🚀 Start Your Journey</a>
            </div>
            <div class="hero-stats">
                <div class="stat"><div class="stat-number">500+</div><div class="stat-label">Problems</div></div>
                <div class="stat"><div class="stat-number">10K+</div><div class="stat-label">Coders</div></div>
                <div class="stat"><div class="stat-number">50+</div><div class="stat-label">Achievements</div></div>
            </div>
        </div>
    </div>
    <section id="features" class="features-section">
        <div class="container">
            <h2 class="section-title">🎯 Game-Changing Features</h2>
            <div class="features-grid">
                <div class="feature-card"><div class="feature-icon">⚡</div><h3>XP & Levels</h3><p>Earn experience points and level up as you solve problems. Every challenge conquered brings you closer to mastery!</p></div>
                <div class="feature-card"><div class="feature-icon">🔥</div><h3>Daily Streaks</h3><p>Build coding habits with streak counters. Maintain your momentum and watch your skills grow exponentially!</p></div>
                <div class="feature-card"><div class="feature-icon">🏆</div><h3>Achievements</h3><p>Unlock badges and achievements for hitting milestones. Show off your coding prowess with visual rewards!</p></div>
            </div>
        </div>
    </section>
</body>
</html>'''

@app.route('/platform')
def platform():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeQuest Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); min-height: 100vh; color: #333; }
        .platform-container { display: flex; flex-direction: column; height: 100vh; }
        .platform-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        .header-left h1 { font-size: 1.5rem; }
        .user-stats { display: flex; gap: 2rem; align-items: center; }
        .stat { text-align: center; }
        .stat-label { font-size: 0.8rem; opacity: 0.8; }
        .stat-value { font-size: 1.2rem; font-weight: bold; }
        .username-input { padding: 0.75rem 1rem; border: none; border-radius: 25px; font-size: 1rem; background: rgba(255,255,255,0.9); min-width: 200px; margin-left: 1rem; }
        .platform-main { display: flex; flex: 1; gap: 1rem; padding: 1rem; overflow: hidden; }
        .problems-section { width: 300px; background: white; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); padding: 1.5rem; }
        .problems-section h2 { color: #667eea; margin-bottom: 1rem; }
        .problems-grid { display: flex; flex-direction: column; gap: 0.5rem; }
        .problem-item { padding: 1rem; border-radius: 10px; cursor: pointer; transition: all 0.3s ease; border-left: 4px solid transparent; }
        .problem-item:hover { background: #f8f9fa; transform: translateX(5px); }
        .problem-item.selected { background: linear-gradient(135deg, #667eea20, #764ba220); border-left-color: #667eea; }
        .problem-item.easy { border-left-color: #28a745; }
        .problem-item.medium { border-left-color: #ffc107; }
        .problem-item.hard { border-left-color: #dc3545; }
        .problem-title { font-weight: bold; margin-bottom: 0.5rem; }
        .problem-meta { display: flex; justify-content: space-between; font-size: 0.8rem; opacity: 0.7; }
        .code-section { flex: 1; display: flex; flex-direction: column; gap: 1rem; }
        .problem-view { background: white; border-radius: 15px; padding: 2rem; box-shadow: 0 8px 25px rgba(0,0,0,0.1); flex: 1; }
        .welcome-screen { text-align: center; padding: 2rem; }
        .welcome-icon { font-size: 4rem; margin-bottom: 1rem; }
        .welcome-screen h2 { color: #667eea; margin-bottom: 1rem; font-size: 2rem; }
        .problem-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; }
        .difficulty-badge { padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.8rem; font-weight: bold; }
        .difficulty-badge.easy { background: #d4edda; color: #155724; }
        .difficulty-badge.medium { background: #fff3cd; color: #856404; }
        .difficulty-badge.hard { background: #f8d7da; color: #721c24; }
        .xp-reward { background: linear-gradient(45deg, #ff6b35, #f7931e); color: white; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.8rem; font-weight: bold; }
        .code-editor { background: white; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); overflow: hidden; flex: 1; display: flex; flex-direction: column; }
        .editor-toolbar { background: #f8f9fa; padding: 1rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; }
        .btn-submit { background: linear-gradient(45deg, #28a745, #20c997); color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; transition: all 0.3s ease; }
        .btn-submit:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
        #code-input { width: 100%; height: 300px; border: none; padding: 1.5rem; font-family: 'Courier New', monospace; font-size: 14px; line-height: 1.5; resize: none; outline: none; background: #fafafa; }
    </style>
</head>
<body>
    <div class="platform-container">
        <header class="platform-header">
            <div class="header-left"><h1>🎮 CodeQuest</h1></div>
            <div class="header-right">
                <div class="user-stats">
                    <div class="stat"><span class="stat-label">Level</span><span class="stat-value" id="user-level">1</span></div>
                    <div class="stat"><span class="stat-label">XP</span><span class="stat-value" id="user-xp">0</span></div>
                    <div class="stat"><span class="stat-label">Streak</span><span class="stat-value" id="user-streak">0</span></div>
                </div>
                <input type="text" id="username" placeholder="Enter username" class="username-input">
                <button onclick="loadUser()" class="btn-submit" style="margin-left: 1rem;">Login</button>
            </div>
        </header>
        <main class="platform-main">
            <div class="problems-section">
                <h2>🎯 Coding Challenges</h2>
                <div class="problems-grid" id="problems-grid"></div>
            </div>
            <div class="code-section">
                <div class="problem-view" id="problem-view">
                    <div class="welcome-screen">
                        <div class="welcome-icon">🎮</div>
                        <h2>Welcome to CodeQuest!</h2>
                        <p>Select a problem from the left to start coding</p>
                    </div>
                    <div id="problem-content" style="display: none;">
                        <div class="problem-header">
                            <div><h3 id="problem-title"></h3></div>
                            <div class="problem-meta">
                                <span class="difficulty-badge" id="problem-difficulty"></span>
                                <span class="xp-reward" id="problem-xp"></span>
                            </div>
                        </div>
                        <div id="problem-description"></div>
                    </div>
                </div>
                <div class="code-editor" id="code-editor" style="display: none;">
                    <div class="editor-toolbar">
                        <span>Python</span>
                        <button onclick="submitSolution()" class="btn-submit">Submit Solution</button>
                    </div>
                    <textarea id="code-input" placeholder="Write your solution here..."></textarea>
                </div>
            </div>
        </main>
    </div>
    <script>
        let currentUser = null;
        let currentProblem = null;
        let problems = {};
        
        document.addEventListener('DOMContentLoaded', function() {
            loadProblems();
        });
        
        async function loadProblems() {
            try {
                const response = await fetch('/api/problems');
                problems = await response.json();
                displayProblems();
            } catch (error) {
                console.error('Error loading problems:', error);
            }
        }
        
        function displayProblems() {
            const problemsGrid = document.getElementById('problems-grid');
            problemsGrid.innerHTML = '';
            
            Object.entries(problems).forEach(([id, problem]) => {
                const problemDiv = document.createElement('div');
                problemDiv.className = `problem-item ${problem.difficulty.toLowerCase()}`;
                problemDiv.onclick = () => selectProblem(id);
                
                problemDiv.innerHTML = `
                    <div class="problem-title">${problem.title}</div>
                    <div class="problem-meta">
                        <span>${problem.difficulty}</span>
                        <span>${problem.xp} XP</span>
                    </div>
                `;
                
                problemsGrid.appendChild(problemDiv);
            });
        }
        
        function selectProblem(problemId) {
            currentProblem = problemId;
            const problem = problems[problemId];
            
            document.querySelectorAll('.problem-item').forEach(item => item.classList.remove('selected'));
            event.target.closest('.problem-item').classList.add('selected');
            
            document.querySelector('.welcome-screen').style.display = 'none';
            document.getElementById('problem-content').style.display = 'block';
            document.getElementById('code-editor').style.display = 'flex';
            
            document.getElementById('problem-title').textContent = problem.title;
            document.getElementById('problem-difficulty').textContent = problem.difficulty;
            document.getElementById('problem-difficulty').className = `difficulty-badge ${problem.difficulty.toLowerCase()}`;
            document.getElementById('problem-xp').textContent = `${problem.xp} XP`;
            
            document.getElementById('problem-description').innerHTML = `
                <p>${problem.description}</p>
                <h4 style="margin-top: 1.5rem; margin-bottom: 1rem; color: #667eea;">Examples:</h4>
                ${problem.examples.map(ex => `
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #667eea;">
                        <strong>Input:</strong> ${ex.input}<br>
                        <strong>Output:</strong> ${ex.output}
                    </div>
                `).join('')}
            `;
            
            document.getElementById('code-input').value = `class Solution:
    def twoSum(self, nums, target):
        # Write your solution here
        pass`;
        }
        
        async function loadUser() {
            const username = document.getElementById('username').value.trim();
            if (!username) {
                alert('Please enter a username!');
                return;
            }
            
            try {
                const response = await fetch(`/api/user/${username}`);
                currentUser = await response.json();
                
                document.getElementById('user-level').textContent = currentUser.level;
                document.getElementById('user-xp').textContent = currentUser.xp;
                document.getElementById('user-streak').textContent = currentUser.streak;
                
                alert(`Welcome ${username}! Level ${currentUser.level}`);
            } catch (error) {
                console.error('Error loading user:', error);
                alert('Error loading user data. Please try again.');
            }
        }
        
        async function submitSolution() {
            if (!currentUser) {
                alert('Please login first!');
                return;
            }
            
            if (!currentProblem) {
                alert('Please select a problem first!');
                return;
            }
            
            const code = document.getElementById('code-input').value;
            if (!code.trim()) {
                alert('Please write some code first!');
                return;
            }
            
            try {
                const response = await fetch('/api/submit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        username: document.getElementById('username').value,
                        problem_id: currentProblem,
                        code: code
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    currentUser = result.user;
                    document.getElementById('user-level').textContent = currentUser.level;
                    document.getElementById('user-xp').textContent = currentUser.xp;
                    document.getElementById('user-streak').textContent = currentUser.streak;
                    alert(`🎉 Success! +${result.xp_gained} XP earned!`);
                } else {
                    alert('❌ Solution failed tests. Try again!');
                }
            } catch (error) {
                console.error('Error submitting solution:', error);
                alert('Error submitting solution. Please try again.');
            }
        }
    </script>
</body>
</html>'''

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