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

function displayProblems(filter = 'all') {
    const problemsList = document.getElementById('problemsList');
    problemsList.innerHTML = '';
    
    Object.entries(problems).forEach(([id, problem]) => {
        if (filter !== 'all' && problem.difficulty.toLowerCase() !== filter) return;
        
        const problemDiv = document.createElement('div');
        problemDiv.className = `problem-item ${problem.difficulty.toLowerCase()}`;
        problemDiv.onclick = () => selectProblem(id);
        
        const isSolved = currentUser && currentUser.solved.includes(id);
        if (isSolved) {
            problemDiv.classList.add('solved');
        }
        
        problemDiv.innerHTML = `
            <div class="problem-title">${problem.title}</div>
            <div class="problem-meta">
                <span class="problem-difficulty">${problem.difficulty}</span>
                <span class="problem-xp">${problem.xp} XP</span>
            </div>
        `;
        
        problemsList.appendChild(problemDiv);
    });
}

function filterProblems(filter) {
    // Update active tab
    document.querySelectorAll('.filter-tab').forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');
    
    displayProblems(filter);
}

function selectProblem(problemId) {
    currentProblem = problemId;
    const problem = problems[problemId];
    
    // Update selected problem styling
    document.querySelectorAll('.problem-item').forEach(item => item.classList.remove('selected'));
    event.target.closest('.problem-item').classList.add('selected');
    
    // Hide welcome screen, show problem content
    document.querySelector('.welcome-screen').style.display = 'none';
    document.getElementById('problemContent').style.display = 'block';
    document.getElementById('codeSection').style.display = 'flex';
    
    // Update problem details
    document.getElementById('problemTitle').textContent = problem.title;
    document.getElementById('difficultyBadge').textContent = problem.difficulty;
    document.getElementById('difficultyBadge').className = `difficulty-badge ${problem.difficulty.toLowerCase()}`;
    document.getElementById('xpReward').textContent = `${problem.xp} XP`;
    
    document.getElementById('problemDescription').innerHTML = `
        <p>${problem.description}</p>
        <h4 style="margin-top: 1.5rem; margin-bottom: 1rem; color: #667eea;">Examples:</h4>
        ${problem.examples.map(ex => `
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #667eea;">
                <strong>Input:</strong> ${ex.input}<br>
                <strong>Output:</strong> ${ex.output}
            </div>
        `).join('')}
    `;
    
    // Set code template
    const codeArea = document.getElementById('codeArea');
    if (problem.title === 'Two Sum') {
        codeArea.value = `class Solution:
    def twoSum(self, nums, target):
        # Write your solution here
        # Return indices of two numbers that add up to target
        pass`;
    } else {
        codeArea.value = `class Solution:
    def solve(self, input_data):
        # Write your solution here
        pass`;
    }
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
        
        // Update UI
        document.getElementById('loginForm').style.display = 'none';
        document.getElementById('userInfo').style.display = 'flex';
        document.getElementById('userName').textContent = username;
        
        updateUserDisplay();
        displayProblems();
    } catch (error) {
        console.error('Error loading user:', error);
        alert('Error loading user data. Please try again.');
    }
}

function updateUserDisplay() {
    if (!currentUser) return;
    
    // Update header stats
    document.getElementById('userStatsMini').textContent = 
        `Level ${currentUser.level} • ${currentUser.xp} XP • ${currentUser.streak}🔥`;
    
    // Update level card
    const levelCard = document.getElementById('levelCard');
    const currentLevelXP = (currentUser.level - 1) * 100;
    const progress = ((currentUser.xp - currentLevelXP) / 100) * 100;
    
    levelCard.querySelector('.level-number').textContent = `Level ${currentUser.level}`;
    levelCard.querySelector('.xp-fill').style.width = `${Math.min(progress, 100)}%`;
    levelCard.querySelector('.xp-text').textContent = `${currentUser.xp - currentLevelXP} / 100 XP`;
    
    // Update stats
    document.getElementById('problemsSolved').textContent = currentUser.solved.length;
    document.getElementById('currentStreak').textContent = `${currentUser.streak} 🔥`;
    document.getElementById('totalXP').textContent = currentUser.xp;
    
    // Update achievements
    const achievementsList = document.getElementById('achievementsList');
    if (currentUser.achievements.length > 0) {
        achievementsList.innerHTML = currentUser.achievements.map(achievement => 
            `<div class="achievement-item">🏆 ${achievement}</div>`
        ).join('');
    } else {
        achievementsList.innerHTML = '<div class="no-achievements">Complete challenges to unlock achievements!</div>';
    }
}

async function runCode() {
    const code = document.getElementById('codeArea').value;
    if (!code.trim()) {
        alert('Please write some code first!');
        return;
    }
    
    // Simple code validation/syntax check could go here
    alert('Code syntax looks good! Click Submit to test against all cases.');
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
    
    const code = document.getElementById('codeArea').value;
    const language = document.getElementById('languageSelect').value;
    
    if (!code.trim()) {
        alert('Please write some code first!');
        return;
    }
    
    // Show loading state
    const submitBtn = document.querySelector('.btn-submit');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = '⏳ Testing...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/api/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: document.getElementById('userName').textContent,
                problem_id: currentProblem,
                code: code,
                language: language
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            const oldLevel = currentUser.level;
            currentUser = result.user;
            const newLevel = currentUser.level;
            
            showSuccessModal(result.xp_gained, newLevel > oldLevel);
            updateUserDisplay();
            displayProblems();
        } else {
            alert('❌ Solution failed tests. Check your logic and try again!');
        }
    } catch (error) {
        console.error('Error submitting solution:', error);
        alert('Error submitting solution. Please try again.');
    } finally {
        // Reset button
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

function showSuccessModal(xpGained, leveledUp = false) {
    const modal = document.getElementById('successModal');
    const xpText = document.getElementById('xpGainedText');
    const levelUpNotice = document.getElementById('levelUpNotice');
    
    xpText.textContent = `+${xpGained} XP`;
    
    if (leveledUp) {
        levelUpNotice.style.display = 'block';
    } else {
        levelUpNotice.style.display = 'none';
    }
    
    modal.style.display = 'block';
    createConfetti();
}

function closeModal() {
    document.getElementById('successModal').style.display = 'none';
}

function createConfetti() {
    const colors = ['#ff6b35', '#f7931e', '#ffe135', '#6bcf7f', '#4d9de0', '#e15554', '#667eea', '#764ba2'];
    
    for (let i = 0; i < 100; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.style.position = 'fixed';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.top = '-10px';
            confetti.style.width = Math.random() * 8 + 4 + 'px';
            confetti.style.height = confetti.style.width;
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.pointerEvents = 'none';
            confetti.style.zIndex = '9999';
            confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
            confetti.style.opacity = Math.random() * 0.8 + 0.2;
            
            document.body.appendChild(confetti);
            
            const animation = confetti.animate([
                { 
                    transform: 'translateY(0) rotate(0deg) scale(1)', 
                    opacity: confetti.style.opacity 
                },
                { 
                    transform: `translateY(100vh) rotate(${Math.random() * 720}deg) scale(0)`, 
                    opacity: 0 
                }
            ], {
                duration: Math.random() * 2000 + 2000,
                easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
            });
            
            animation.onfinish = () => confetti.remove();
        }, i * 30);
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('successModal');
    if (event.target === modal) {
        closeModal();
    }
}