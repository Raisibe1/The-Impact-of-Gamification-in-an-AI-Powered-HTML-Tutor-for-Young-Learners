// ===== DRAG & DROP SYSTEM =====
let dragData = null;

document.addEventListener('DOMContentLoaded', () => {
    // Set up drag events
    document.querySelectorAll('.drag-item').forEach(item => {
        item.addEventListener('dragstart', (e) => {
            dragData = item.dataset.term;
            item.classList.add('dragging');
        });
        item.addEventListener('dragend', (e) => {
            item.classList.remove('dragging');
        });
    });

    document.querySelectorAll('.drop-zone').forEach(zone => {
        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('drag-over');
        });
        zone.addEventListener('dragleave', (e) => {
            zone.classList.remove('drag-over');
        });
        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('drag-over');
            if (dragData) {
                zone.dataset.dropped = dragData;
                zone.innerHTML = `<span style="color: #48bb78;">✅ ${dragData}</span>`;
                zone.style.borderColor = '#48bb78';
                dragData = null;
            }
        });
    });

    // Load saved progress
    loadProgress();
    updateDisplay();
});

// ===== VISUAL MATCH CHECK =====
function checkVisualMatch() {
    const zones = document.querySelectorAll('.drop-zone');
    let correct = 0;
    let total = zones.length;

    zones.forEach(zone => {
        const dropped = zone.dataset.dropped;
        const expected = zone.dataset.expected;
        if (dropped === expected) {
            zone.classList.add('correct');
            zone.classList.remove('incorrect');
            correct++;
        } else if (dropped) {
            zone.classList.add('incorrect');
            zone.classList.remove('correct');
        }
    });

    const feedback = document.getElementById('visual-match-feedback');
    if (correct === total) {
        feedback.innerHTML = `
                    <div class="gamification-feedback success">
                        <div class="feedback-title">🎉 Perfect! +25 XP</div>
                        <div class="feedback-detail">You've mastered visual design elements!</div>
                    </div>
                `;
        addXP(25);
    } else {
        feedback.innerHTML = `
                    <div class="gamification-feedback hint">
                        <div class="feedback-title">💡 Keep Going!</div>
                        <div class="feedback-detail">You got ${correct}/${total} correct. Try again!</div>
                    </div>
                `;
    }
}

function resetVisualMatch() {
    document.querySelectorAll('.drop-zone').forEach(zone => {
        const expected = zone.dataset.expected;
        const labels = {
            'color': 'The hue that evokes emotion',
            'size': 'How big or small elements appear',
            'space': 'The area around or between elements',
            'position': 'Where elements are placed on the page',
            'repetition': 'Patterns that create unity'
        };
        zone.innerHTML = `<span class="placeholder">Drop here: ${labels[expected] || expected}</span>`;
        zone.dataset.dropped = '';
        zone.className = 'drop-zone';
    });
    document.getElementById('visual-match-feedback').innerHTML = '';
}

// ===== GOAL MATCHING =====
function checkGoalMatch(select) {
    const parent = select.closest('.match-item');
    const isCorrect = select.value === select.dataset.correct;
    select.classList.remove('correct', 'incorrect');
    if (select.value) {
        select.classList.add(isCorrect ? 'correct' : 'incorrect');
    }
    updateGoalFeedback();
}

function updateGoalFeedback() {
    const selects = document.querySelectorAll('#goal-matching select');
    let correct = 0;
    let total = selects.length;
    let filled = 0;

    selects.forEach(sel => {
        if (sel.value) {
            filled++;
            if (sel.value === sel.dataset.correct) correct++;
        }
    });

    const feedback = document.getElementById('goal-match-feedback');
    if (filled === total) {
        if (correct === total) {
            feedback.innerHTML = `
                        <div class="gamification-feedback success">
                            <div class="feedback-title">🎉 Excellent! +25 XP</div>
                            <div class="feedback-detail">You understand user vs site goals!</div>
                        </div>
                    `;
            addXP(25);
        } else {
            feedback.innerHTML = `
                        <div class="gamification-feedback hint">
                            <div class="feedback-title">💡 Almost There!</div>
                            <div class="feedback-detail">You got ${correct}/${total} correct. Review the examples above.</div>
                        </div>
                    `;
        }
    }
}

// ===== DESIGN INTENT =====
function showDesignIntent() {
    document.getElementById('design-intent-result').innerHTML = `
                <span style="color: #48bb78;">💡 Designers make choices to create an outcome—in action or feeling for the user. All designers have plans and intentions!</span>
            `;
}

// ===== STEP COMPLETION =====
const completedSteps = new Set();

function completeStep(stepId) {
    if (!completedSteps.has(stepId)) {
        completedSteps.add(stepId);
        addXP(15);
        document.getElementById(`${stepId}-feedback`).innerHTML = `
                    <div class="gamification-feedback success">
                        <div class="feedback-title">✅ Step Complete! +15 XP</div>
                        <div class="feedback-detail">Great progress! Keep going!</div>
                    </div>
                `;
        updateStepProgress();
        saveProgress();
    } else {
        document.getElementById(`${stepId}-feedback`).innerHTML = `
                    <div class="gamification-feedback hint">
                        <div class="feedback-title">💡 Already Completed</div>
                        <div class="feedback-detail">You've already finished this step!</div>
                    </div>
                `;
    }
}

function updateStepProgress() {
    const total = 4;
    const count = completedSteps.size;
    document.getElementById('step-progress').textContent = `${count}/${total}`;
}

// ===== XP SYSTEM =====
function addXP(amount) {
    const xpEl = document.getElementById('xp-count');
    const levelEl = document.getElementById('level-count');
    let xp = parseInt(localStorage.getItem('design_xp') || '0');
    let level = parseInt(localStorage.getItem('design_level') || '1');

    xp += amount;
    const newLevel = Math.floor(xp / 100) + 1;
    if (newLevel > level) {
        level = newLevel;
        showLevelUp(level);
    }

    localStorage.setItem('design_xp', xp);
    localStorage.setItem('design_level', level);

    if (xpEl) xpEl.textContent = xp;
    if (levelEl) levelEl.textContent = level;
}

function updateDisplay() {
    const xp = parseInt(localStorage.getItem('design_xp') || '0');
    const level = parseInt(localStorage.getItem('design_level') || '1');
    document.getElementById('xp-count').textContent = xp;
    document.getElementById('level-count').textContent = level;
}

function showLevelUp(level) {
    const overlay = document.createElement('div');
    overlay.className = 'level-up-overlay';
    overlay.innerHTML = `
                <div class="level-up-modal">
                    <span class="level-up-icon">🎉</span>
                    <h2>Level ${level}!</h2>
                    <p>You've reached Level ${level} in Web Design!</p>
                    <button class="btn btn-primary" onclick="this.closest('.level-up-overlay').remove()">
                        Continue Learning 🚀
                    </button>
                </div>
            `;
    document.body.appendChild(overlay);
}

// ===== SAVE / LOAD =====
function saveProgress() {
    localStorage.setItem('design_completed_steps', JSON.stringify([...completedSteps]));
}

function loadProgress() {
    const saved = localStorage.getItem('design_completed_steps');
    if (saved) {
        try {
            const steps = JSON.parse(saved);
            steps.forEach(step => completedSteps.add(step));
            updateStepProgress();
            steps.forEach(step => {
                const feedback = document.getElementById(`${step}-feedback`);
                if (feedback) {
                    feedback.innerHTML = `
                                <div class="gamification-feedback success">
                                    <div class="feedback-title">✅ Step Complete!</div>
                                    <div class="feedback-detail">You completed this step earlier.</div>
                                </div>
                            `;
                }
            });
        } catch (e) { }
    }
}