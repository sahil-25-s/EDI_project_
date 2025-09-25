let currentUser = null;
let currentProblem = null;
let problems = {};

// Load problems on page load
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
    const problemsList = document.getElementById('problemsList');
    problemsList.innerHTML = '';
    
    Object.entries(problems).forEach(([id, problem]) => {
        const problemDiv = document.createElement('div');
        problemDiv.className = `problem-item ${problem.difficulty.toLowerCase()}`;
        problemDiv.onclick = () => selectProblem(id);
        
        const isSolved = currentUser && currentUser.solved.includes(id);
        if (isSolved) {
            problemDiv.classList.add('solved');
        }
        
        problemDiv.innerHTML = `
            <div class="problem-title">${isSolved ? '✅ ' : ''}${problem.title}</div>
            <div class="problem-difficulty">${problem.difficulty} • ${problem.xp} XP</div>
        `;
        
        problemsList.appendChild(problemDiv);
    });
}

function selectProblem(problemId) {
    currentProblem = problemId;
    const problem = problems[problemId];
    
    const problemDetails = document.getElementById('problemDetails');
    problemDetails.innerHTML = `
        <h2>${problem.title}</h2>
        <div class="difficulty-badge ${problem.difficulty.toLowerCase()}">${problem.difficulty}</div>
        <p>${problem.description}</p>
        <h4>Example:</h4>
        ${problem.examples.map(ex => `
            <div class="example">
                <strong>Input:</strong> ${ex.input}<br>
                <strong>Output:</strong> ${ex.output}
            </div>
        `).join('')}
    `;
    
    document.getElementById('codeEditor').style.display = 'flex';
    
    // Set default code template
    const codeArea = document.getElementById('codeArea');
    if (problem.title === 'Two Sum') {
        codeArea.value = `class Solution:
    def twoSum(self, nums, target):
        # Your code here
        pass`;
    } else {
        codeArea.value = `class Solution:
    def solve(self, input_data):
        # Your code here
        pass`;
    }
}

async function loadUser() {
    const username = document.getElementById('username').value.trim();
    if (!username) return;
    
    try {
        const response = await fetch(`/api/user/${username}`);
        currentUser = await response.json();
        updateUserDisplay();
        displayProblems(); // Refresh to show solved problems
    } catch (error) {
        console.error('Error loading user:', error);
    }
}

function updateUserDisplay() {
    if (!currentUser) return;
    
    const userStats = document.getElementById('userStats');
    userStats.innerHTML = `
        <div class="user-info">
            <span class="user-level">Level ${currentUser.level}</span>
            <span class="user-xp">${currentUser.xp} XP</span>
            <span>🔥 ${currentUser.streak}</span>
        </div>
    `;
    
    // Update level display
    const levelDisplay = document.getElementById('levelDisplay');
    const currentLevelXP = (currentUser.level - 1) * 100;
    const nextLevelXP = currentUser.level * 100;
    const progress = ((currentUser.xp - currentLevelXP) / 100) * 100;
    
    levelDisplay.innerHTML = `
        <div class="level">Level ${currentUser.level}</div>
        <div class="xp-bar">
            <div class="xp-fill" style="width: ${progress}%"></div>
        </div>
        <div class="xp-text">${currentUser.xp - currentLevelXP} / 100 XP</div>
    `;
    
    // Update achievements
    const achievementsList = document.querySelector('.achievement-list');
    achievementsList.innerHTML = currentUser.achievements.map(achievement => 
        `<div class="achievement-item">🏆 ${achievement}</div>`
    ).join('');
    
    // Update streak
    document.querySelector('.streak-number').textContent = `${currentUser.streak} days`;
}

async function submitSolution() {
    if (!currentUser || !currentProblem) {
        alert('Please login and select a problem first!');
        return;
    }
    
    const code = document.getElementById('codeArea').value;
    const language = document.getElementById('languageSelect').value;
    
    if (!code.trim()) {
        alert('Please write some code first!');
        return;
    }
    
    try {
        const response = await fetch('/api/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: document.getElementById('username').value,
                problem_id: currentProblem,
                code: code,
                language: language
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentUser = result.user;
            showSuccessModal(result.xp_gained);
            updateUserDisplay();
            displayProblems();
        } else {
            alert('Solution failed tests. Try again!');
        }
    } catch (error) {
        console.error('Error submitting solution:', error);
        alert('Error submitting solution. Please try again.');
    }
}

function showSuccessModal(xpGained) {
    const modal = document.getElementById('successModal');
    const xpText = document.getElementById('xpGained');
    xpText.textContent = `+${xpGained} XP gained!`;
    modal.style.display = 'block';
    
    // Add confetti effect
    createConfetti();
}

function closeModal() {
    document.getElementById('successModal').style.display = 'none';
}

function createConfetti() {
    const colors = ['#ff6b35', '#f7931e', '#ffe135', '#6bcf7f', '#4d9de0', '#e15554'];
    
    for (let i = 0; i < 50; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.style.position = 'fixed';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.top = '-10px';
            confetti.style.width = '10px';
            confetti.style.height = '10px';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.pointerEvents = 'none';
            confetti.style.zIndex = '9999';
            confetti.style.borderRadius = '50%';
            
            document.body.appendChild(confetti);
            
            const animation = confetti.animate([
                { transform: 'translateY(0) rotate(0deg)', opacity: 1 },
                { transform: `translateY(100vh) rotate(720deg)`, opacity: 0 }
            ], {
                duration: 3000,
                easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
            });
            
            animation.onfinish = () => confetti.remove();
        }, i * 50);
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('successModal');
    if (event.target === modal) {
        closeModal();
    }
}