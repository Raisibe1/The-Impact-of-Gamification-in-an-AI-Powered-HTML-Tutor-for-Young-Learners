// ============================================================
// WEB DEV QUEST - Gamified Web Development Learning Platform
// ============================================================

const CONFIG = {
    xpPerLevel: 100,
    xpPerChallenge: 50,
    challengeBonus: 25
};

// ============================================================
// USER STATE
// ============================================================

let userState = {
    xp: 0,
    level: 1,
    streak: 0,
    badges: [],
    completedLessons: [],
    completedChallenges: [],
    currentLesson: 'html'
};

// ============================================================
// LESSON DATA
// ============================================================

const LESSONS = {
    html: {
        id: 'html',
        title: 'HTML Basics',
        badge: 'HTML',
        xp: 100,
        concept: `
            HTML (HyperText Markup Language) is the foundation
            of every web page. It uses <strong>tags</strong>
            to structure content.
        `,
        visual: {
            type: 'html',
            html: `
                <h1>Hello World!</h1>
                <p>This is a paragraph.</p>
                <a href="#">Click me!</a>
            `
        },
        challenge: {
            title: 'Create Your First Heading',
            description: 'Write an HTML heading tag with your name:',
            starterCode: '<h1>Your Name</h1>',
            solution: '<h1>Web Dev Student</h1>',
            test: (code) =>
                code.includes('<h1') &&
                code.includes('</h1>') &&
                code.length > 10,
            hint: 'Try: <h1>Your Name</h1>',
            xp: 50
        },
        nextLesson: 'css'
    },
    css: {
        id: 'css',
        title: 'CSS Styling',
        badge: 'CSS',
        xp: 150,
        concept: `
            CSS (Cascading Style Sheets) controls the
            <strong>look and feel</strong> of your HTML.
            You can change colors, fonts, spacing and layout.
        `,
        visual: {
            type: 'css',
            html: `
                <h1>Hello World!</h1>
                <p>CSS changes how HTML looks.</p>
            `,
            css: `
                h1 {
                    color: blue;
                    text-align: center;
                }
                p {
                    color: #555;
                    text-align: center;
                }
            `
        },
        challenge: {
            title: 'Style Your Heading',
            description: 'Add CSS to make your heading blue and centered:',
            starterCode: `h1 {
    /* Add styles here */
}`,
            solution: `h1 {
    color: blue;
    text-align: center;
}`,
            test: (code) =>
                code.includes('color') &&
                (code.includes('blue') || code.includes('#0000ff')) &&
                code.includes('text-align'),
            hint: 'Use "color: blue;" and "text-align: center;"',
            xp: 50
        },
        nextLesson: 'js'
    },
    js: {
        id: 'js',
        title: 'JavaScript Logic',
        badge: 'JS',
        xp: 200,
        concept: `
            JavaScript adds <strong>interactivity</strong>
            to web pages. Functions let you write reusable code.
        `,
        visual: {
            type: 'js',
            html: `
                <h2 id="greeting">Hello Student!</h2>
                <button id="demoButton">Click Me</button>
            `,
            js: `
                const button = document.getElementById('demoButton');
                const greeting = document.getElementById('greeting');
                button.addEventListener('click', function() {
                    greeting.textContent = 'JavaScript is working!';
                });
            `
        },
        challenge: {
            title: 'Write a Greeting Function',
            description: 'Write a function that takes a name and returns "Hello [name]!":',
            starterCode: `function greet(name) {
    // Your code here
}`,
            solution: `function greet(name) {
    return "Hello " + name + "!";
}`,
            test: (code) =>
                code.includes('function') &&
                code.includes('return') &&
                code.includes('name'),
            hint: 'Use: return "Hello " + name + "!"',
            xp: 75
        },
        nextLesson: 'react'
    },
    react: {
        id: 'react',
        title: 'React Components',
        badge: 'React',
        xp: 300,
        concept: `
            React is a library for building
            <strong>user interfaces</strong>
            using reusable components.
        `,
        visual: {
            type: 'react',
            html: `
                <div class="react-label">⚛ React Component</div>
                <div class="react-card">
                    <h2>Hello, Student!</h2>
                    <p>This is a reusable React component.</p>
                </div>
            `
        },
        challenge: {
            title: 'Create a React Component',
            description: 'Write a React component that displays a greeting:',
            starterCode: `function Welcome(props) {
    return (
        <div>
            {/* Your code here */}
        </div>
    );
}`,
            solution: `function Welcome(props) {
    return <h1>Hello, {props.name}!</h1>;
}`,
            test: (code) =>
                code.includes('function') &&
                code.includes('return') &&
                code.includes('props'),
            hint: 'Use: return <h1>Hello, {props.name}!</h1>;',
            xp: 100
        },
        nextLesson: null
    }
};

// ============================================================
// BADGES
// ============================================================

const BADGES = {
    html: {
        id: 'html',
        name: 'HTML Builder',
        description: 'Completed HTML Basics'
    },
    css: {
        id: 'css',
        name: 'CSS Stylist',
        description: 'Styled your first element'
    },
    js: {
        id: 'js',
        name: 'JS Master',
        description: 'Wrote your first function'
    },
    react: {
        id: 'react',
        name: 'React Developer',
        description: 'Built your first component'
    },
    'level-5': {
        id: 'level-5',
        name: 'Level 5 Achieved',
        description: 'Reached level 5'
    },
    'level-10': {
        id: 'level-10',
        name: 'Level 10 Achieved',
        description: 'Reached level 10'
    }
};

// ============================================================
// DOM REFERENCES
// ============================================================

const DOM = {};

// ============================================================
// INITIALIZATION
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    DOM.xpCount = document.getElementById('xp-count');
    DOM.levelCount = document.getElementById('level-count');
    DOM.streakCount = document.getElementById('streak-count');
    DOM.badgeCount = document.getElementById('badge-count');
    DOM.lessonContainer = document.getElementById('lesson-container');
    loadState();
    setupPathNavigation();
    loadLesson(userState.currentLesson);
    updateStats();
    startStreakTimer();
});

// ============================================================
// STATE MANAGEMENT
// ============================================================

function loadState() {
    const saved = localStorage.getItem('webdevquest_state');
    if (!saved) return;
    try {
        const parsed = JSON.parse(saved);
        userState = { ...userState, ...parsed };
    } catch (error) {
        console.warn('Failed to load saved state:', error);
    }
}

function saveState() {
    localStorage.setItem('webdevquest_state', JSON.stringify(userState));
}

// ============================================================
// GAME STATS
// ============================================================

function updateStats() {
    if (DOM.xpCount) DOM.xpCount.textContent = userState.xp;
    if (DOM.levelCount) DOM.levelCount.textContent = userState.level;
    if (DOM.streakCount) DOM.streakCount.textContent = userState.streak;
    if (DOM.badgeCount) DOM.badgeCount.textContent = userState.badges.length;
}

// ============================================================
// XP SYSTEM
// ============================================================

function addXP(amount) {
    userState.xp += amount;
    const newLevel = Math.floor(userState.xp / CONFIG.xpPerLevel) + 1;
    if (newLevel > userState.level) {
        userState.level = newLevel;
        showLevelUp(userState.level);
        checkLevelBadges(userState.level);
    }
    updateStreak();
    updateStats();
    saveState();
}

// ============================================================
// STREAK SYSTEM
// ============================================================

function updateStreak() {
    const lastActive = localStorage.getItem('webdevquest_last_active');
    const today = new Date().toDateString();
    if (lastActive === today) return;
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    userState.streak = lastActive === yesterday.toDateString()
        ? userState.streak + 1
        : 1;
    localStorage.setItem('webdevquest_last_active', today);
    saveState();
}

function startStreakTimer() {
    setInterval(() => {
        updateStreak();
        updateStats();
    }, 3600000);
}

// ============================================================
// BADGES
// ============================================================

function unlockBadge(badgeId) {
    if (userState.badges.includes(badgeId)) return;
    userState.badges.push(badgeId);
    updateStats();
    saveState();
    const badge = BADGES[badgeId];
    if (badge) showNotification(`Badge Unlocked: ${badge.name}`, badge.description);
}

function checkLevelBadges(level) {
    if (level >= 5) unlockBadge('level-5');
    if (level >= 10) unlockBadge('level-10');
}

// ============================================================
// LESSON LOADING
// ============================================================

function loadLesson(lessonId) {
    const lesson = LESSONS[lessonId];
    if (!lesson) return;
    userState.currentLesson = lessonId;
    saveState();
    document.querySelectorAll('.path-node').forEach(node => {
        node.classList.remove('active');
        if (node.dataset.lesson === lessonId) node.classList.add('active');
    });
    renderLesson(lesson);
}

// ============================================================
// RENDER LESSON
// ============================================================

function renderLesson(lesson) {
    const html = `
        <div class="lesson" id="lesson-${lesson.id}">
            <div class="lesson-header">
                <h2>${lesson.title}<span class="lesson-badge">${lesson.badge}</span></h2>
                <span class="lesson-xp">${lesson.xp} XP</span>
            </div>
            <div class="lesson-content">
                <div class="concept-box">
                    <p>${lesson.concept}</p>
                </div>
                <h4 class="visual-title">Visual Concept</h4>
                <div class="visual-concept" id="visual-${lesson.id}">
                    ${renderVisualConcept(lesson)}
                </div>
                <div class="challenge-area">
                    <h3>${lesson.challenge.title}</h3>
                    <p class="challenge-desc">${lesson.challenge.description}</p>
                    <div class="code-editor-container">
                        <textarea class="code-editor" id="challenge-editor" spellcheck="false">${lesson.challenge.starterCode}</textarea>
                    </div>
                    <div class="button-group">
                        <button class="btn btn-primary" onclick="runChallenge('${lesson.id}')">Run Code</button>
                        <button class="btn btn-secondary" onclick="showHint('${lesson.id}')">Hint</button>
                        <button class="btn btn-secondary" onclick="resetChallenge('${lesson.id}')">Reset</button>
                    </div>
                    <div class="output-console" id="output-console">
                        <div class="log-line">Ready to run your code...</div>
                    </div>
                    <div id="feedback-container"></div>
                </div>
                
                ${
                    lesson.nextLesson
                        ? `
                        <div class="next-lesson-container" style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
                            <button class="btn btn-success" id="next-lesson-btn" style="display:none;" onclick="loadLesson('${lesson.nextLesson}')">
                                Next Lesson →
                            </button>
                            <button class="btn btn-primary" id="next-level-btn" style="display:none;" onclick="window.location.href='/program'">
                                🚀 Next Level
                            </button>
                        </div>`
                        : `
                        <div class="completion-box">
                            <h3>You've Completed All Lessons!</h3>
                            <p>You're now a certified Web Developer!</p>
                            <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-top: 12px;">
                                <button class="btn btn-primary" onclick="resetAllProgress()">Start Over</button>
                                <button class="btn btn-success" onclick="window.location.href='/test'">🚀 Next Level</button>
                            </div>
                        </div>`
                }
            </div>
        </div>
    `;
    DOM.lessonContainer.innerHTML = html;
    initializeVisualConcept(lesson);
    updatePath();
}

// ============================================================
// VISUAL CONCEPT ROUTER
// ============================================================

function renderVisualConcept(lesson) {
    const visual = lesson.visual;
    if (!visual) return '<div class="block-error">No visual concept available.</div>';
    switch (visual.type) {
        case 'html':
            return createHTMLVisual(visual);
        case 'css':
            return createCSSVisual(visual);
        case 'js':
            return createJSVisual(visual);
        case 'react':
            return createReactVisual(visual);
        default:
            return '<div class="block-error">Unknown visual type.</div>';
    }
}

// ============================================================
// HTML VISUAL
// ============================================================

function createHTMLVisual(visual) {
    return `
        <div class="visual-browser">
            <div class="browser-bar">
                <span class="browser-dot"></span>
                <span class="browser-dot"></span>
                <span class="browser-dot"></span>
                <span class="browser-address">webdevquest.local</span>
            </div>
            <div class="browser-content html-demo">
                ${visual.html}
            </div>
        </div>
    `;
}

// ============================================================
// CSS VISUAL
// ============================================================

function createCSSVisual(visual) {
    return `
        <div class="visual-browser">
            <div class="browser-bar">
                <span class="browser-dot"></span>
                <span class="browser-dot"></span>
                <span class="browser-dot"></span>
                <span class="browser-address">webdevquest.local</span>
            </div>
            <div class="browser-content css-demo">
                <style>${visual.css}</style>
                ${visual.html}
            </div>
        </div>
    `;
}

// ============================================================
// JAVASCRIPT VISUAL
// ============================================================

function createJSVisual(visual) {
    return `
        <div class="visual-browser">
            <div class="browser-bar">
                <span class="browser-dot"></span>
                <span class="browser-dot"></span>
                <span class="browser-dot"></span>
                <span class="browser-address">webdevquest.local</span>
            </div>
            <div class="browser-content js-demo">
                ${visual.html}
            </div>
        </div>
    `;
}

// ============================================================
// REACT VISUAL
// ============================================================

function createReactVisual(visual) {
    return `
        <div class="visual-browser">
            <div class="browser-bar">
                <span class="browser-dot"></span>
                <span class="browser-dot"></span>
                <span class="browser-dot"></span>
                <span class="browser-address">react.quest</span>
            </div>
            <div class="browser-content react-demo">
                ${visual.html}
            </div>
        </div>
    `;
}

// ============================================================
// INITIALIZE JAVASCRIPT VISUAL
// ============================================================

function initializeVisualConcept(lesson) {
    if (!lesson.visual || lesson.visual.type !== 'js') return;
    const container = document.querySelector(`#visual-${lesson.id}`);
    if (!container) return;
    const button = container.querySelector('#demoButton');
    const greeting = container.querySelector('#greeting');
    if (button && greeting) {
        button.addEventListener('click', () => {
            greeting.textContent = 'JavaScript is working!';
        });
    }
}

// ============================================================
// CHALLENGE SYSTEM
// ============================================================

function runChallenge(lessonId) {
    const lesson = LESSONS[lessonId];
    if (!lesson) return;
    const editor = document.getElementById('challenge-editor');
    const consoleElement = document.getElementById('output-console');
    const feedback = document.getElementById('feedback-container');
    const nextBtn = document.getElementById('next-lesson-btn');
    if (!editor || !consoleElement || !feedback) return;
    const code = editor.value.trim();
    consoleElement.innerHTML = '';
    feedback.innerHTML = '';
    addConsoleLog(consoleElement, 'Running your code...');
    try {
        const isValid = lesson.challenge.test(code);
        if (isValid) {
            addConsoleLog(consoleElement, 'Challenge completed!', 'success');
            const alreadyCompleted = userState.completedChallenges.includes(lessonId);
            if (!alreadyCompleted) {
                addConsoleLog(consoleElement, `+${lesson.challenge.xp} XP awarded!`, 'success');
                userState.completedChallenges.push(lessonId);
                addXP(lesson.challenge.xp);
            } else {
                addConsoleLog(consoleElement, 'Challenge already completed. XP was already awarded.', 'success');
            }
            feedback.innerHTML = `
                <div class="gamification-feedback success">
                    <div class="feedback-title">Perfect!</div>
                    <div class="feedback-detail">You've mastered this concept.</div>
                </div>
            `;
            if (!userState.completedLessons.includes(lessonId)) {
                userState.completedLessons.push(lessonId);
                unlockBadge(lessonId);
                saveState();
                updatePath();
            }
            if (lesson.nextLesson && nextBtn) {
                nextBtn.style.display = 'inline-flex';
            }
            markLessonComplete(lessonId);
            saveState();
        } else {
            addConsoleLog(consoleElement, 'Not quite right. Try again!', 'error');
            feedback.innerHTML = `
                <div class="gamification-feedback error">
                    <div class="feedback-title">Not quite right</div>
                    <div class="feedback-detail">Check your code and try again. Use the hint if you're stuck!</div>
                </div>
            `;
        }
    } catch (error) {
        addConsoleLog(consoleElement, `Error: ${error.message}`, 'error');
        feedback.innerHTML = `
            <div class="gamification-feedback error">
                <div class="feedback-title">Something went wrong</div>
                <div class="feedback-detail">${escapeHtml(error.message)}</div>
            </div>
        `;
    }
}

// ============================================================
// CONSOLE
// ============================================================

function addConsoleLog(consoleElement, message, type = '') {
    const line = document.createElement('div');
    line.className = `log-line ${type}`;
    line.textContent = message;
    consoleElement.appendChild(line);
    consoleElement.scrollTop = consoleElement.scrollHeight;
}

// ============================================================
// HINT SYSTEM
// ============================================================

function showHint(lessonId) {
    const lesson = LESSONS[lessonId];
    if (!lesson) return;
    const feedback = document.getElementById('feedback-container');
    if (!feedback) return;
    feedback.innerHTML = `
        <div class="gamification-feedback hint">
            <div class="feedback-title">Hint</div>
            <div class="feedback-detail">${escapeHtml(lesson.challenge.hint)}</div>
            <pre class="hint-code">${escapeHtml(lesson.challenge.hint)}</pre>
        </div>
    `;
}

// ============================================================
// RESET CHALLENGE
// ============================================================

function resetChallenge(lessonId) {
    const lesson = LESSONS[lessonId];
    if (!lesson) return;
    const editor = document.getElementById('challenge-editor');
    const consoleElement = document.getElementById('output-console');
    const feedback = document.getElementById('feedback-container');
    if (editor) editor.value = lesson.challenge.starterCode;
    if (consoleElement) {
        consoleElement.innerHTML = `
            <div class="log-line">Ready to run your code...</div>
        `;
    }
    if (feedback) feedback.innerHTML = '';
}

// ============================================================
// LESSON PROGRESS
// ============================================================

function markLessonComplete(lessonId) {
    const node = document.querySelector(`.path-node[data-lesson="${lessonId}"]`);
    if (!node) return;
    node.classList.remove('active');
    node.classList.add('completed');
    const status = node.querySelector('.node-status');
    if (status) status.textContent = '✓';

    // Show both buttons
    const nextBtn = document.getElementById('next-lesson-btn');
    const levelBtn = document.getElementById('next-level-btn');
    if (nextBtn) nextBtn.style.display = 'inline-flex';
    if (levelBtn) levelBtn.style.display = 'inline-flex';
}

function updatePath() {
    document.querySelectorAll('.path-node').forEach(node => {
        const lessonId = node.dataset.lesson;
        if (userState.completedLessons.includes(lessonId)) {
            node.classList.add('completed');
            node.classList.remove('active', 'locked');
            const status = node.querySelector('.node-status');
            if (status) status.textContent = '✓';
            return;
        }
        if (lessonId === userState.currentLesson) {
            node.classList.add('active');
            node.classList.remove('locked');
            const status = node.querySelector('.node-status');
            if (status) status.textContent = '▶';
            return;
        }
        const previousLesson = getPreviousLesson(lessonId);
        if (previousLesson && userState.completedLessons.includes(previousLesson)) {
            node.classList.remove('locked');
            const status = node.querySelector('.node-status');
            if (status) status.textContent = '🔓';
        } else {
            node.classList.add('locked');
            const status = node.querySelector('.node-status');
            if (status) status.textContent = '🔒';
        }
    });
}

function getPreviousLesson(lessonId) {
    const keys = Object.keys(LESSONS);
    const index = keys.indexOf(lessonId);
    return index > 0 ? keys[index - 1] : null;
}

// ============================================================
// PATH NAVIGATION
// ============================================================

function setupPathNavigation() {
    document.querySelectorAll('.path-node').forEach(node => {
        node.addEventListener('click', () => {
            const lessonId = node.dataset.lesson;
            if (node.classList.contains('locked')) return;
            loadLesson(lessonId);
        });
    });
}

// ============================================================
// NOTIFICATIONS
// ============================================================

function showNotification(title, message) {
    const notification = document.createElement('div');
    notification.className = 'quest-notification';
    notification.innerHTML = `
        <div class="notification-title">${escapeHtml(title)}</div>
        <div class="notification-message">${escapeHtml(message)}</div>
    `;
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transition = 'opacity 0.5s ease';
        setTimeout(() => notification.remove(), 500);
    }, 4000);
}

// ============================================================
// LEVEL UP
// ============================================================

function showLevelUp(level) {
    const overlay = document.createElement('div');
    overlay.className = 'level-up-overlay';
    overlay.innerHTML = `
        <div class="level-up-modal">
            <span class="level-up-icon">🏆</span>
            <h2>Level ${level}!</h2>
            <p>You've reached Level ${level}! Keep coding and keep learning.</p>
            <button class="btn btn-primary" onclick="this.closest('.level-up-overlay').remove()">
                Continue Coding
            </button>
        </div>
    `;
    document.body.appendChild(overlay);
}

// ============================================================
// RESET ALL PROGRESS
// ============================================================

function resetAllProgress() {
    const confirmed = confirm(
        'Reset all progress? This will delete your XP, badges, completed lessons and challenges.'
    );
    if (!confirmed) return;
    localStorage.removeItem('webdevquest_state');
    localStorage.removeItem('webdevquest_last_active');
    userState = {
        xp: 0,
        level: 1,
        streak: 0,
        badges: [],
        completedLessons: [],
        completedChallenges: [],
        currentLesson: 'html'
    };
    saveState();
    updateStats();
    loadLesson('html');
    location.reload();
}

// ============================================================
// SECURITY HELPER
// ============================================================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ============================================================
// GLOBAL FUNCTIONS
// ============================================================

window.loadLesson = loadLesson;
window.runChallenge = runChallenge;
window.showHint = showHint;
window.resetChallenge = resetChallenge;
window.resetAllProgress = resetAllProgress;

console.log('🚀 Web Dev Quest loaded!');
console.log('📚 Available lessons:', Object.keys(LESSONS));
console.log('🎮 Gamification engine ready!');