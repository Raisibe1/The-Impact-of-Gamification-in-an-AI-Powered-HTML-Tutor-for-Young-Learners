import { PageShell } from './page_shell.js';
import { STEP_LESSONS } from './lesson_steps.js';

class ListsTablesPage extends PageShell {
    constructor() {
        super({
            lessonSlug: 'lists',
            steps: STEP_LESSONS.lists?.steps || [],
        });
        this._answeredMCQs = new Set();
        this._completedSteps = new Set();
    }

    async start() {
        await super.start();
        this._restoreData();
        this._updateProgress();
    }

    // =========================================================
    // ---- ACTIVITY 1: Ordered List Builder ----
    // =========================================================
    buildOrderedList() {
        const titleEl = document.getElementById('ol-title');
        const typeEl  = document.getElementById('ol-type');
        const itemsEl = document.getElementById('ol-items');

        const title = (titleEl?.value || '').trim();
        const type  = (typeEl?.value  || '').trim();
        const raw   = (itemsEl?.value || '').trim();

        const items = raw
            .split('\n')
            .map(s => s.trim())
            .filter(Boolean);

        if (items.length === 0) {
            const codeEl = document.getElementById('ol-code');
            if (codeEl) codeEl.textContent = 'Add at least one item first…';
            return;
        }

        // Build the code output (as text)
        const attr = type ? ` type="${type}"` : '';
        const lines = items.map(i => `  <li>${i}</li>`).join('\n');
        const codeStr = `<ol${attr}>\n${lines}\n</ol>`;

        const codeEl = document.getElementById('ol-code');
        if (codeEl) codeEl.textContent = codeStr;

        // Build the live preview safely
        const wrap    = document.getElementById('ol-preview-wrap');
        const preview = document.getElementById('ol-preview');
        if (wrap && preview) {
            preview.innerHTML = '';

            if (title) {
                const h = document.createElement('h4');
                h.textContent = title;
                h.style.color = '#f6ad55';
                h.style.marginBottom = '8px';
                preview.appendChild(h);
            }

            const ol = document.createElement('ol');
            if (type) ol.setAttribute('type', type);
            ol.style.color = '#cbd5e0';
            ol.style.paddingLeft = '22px';
            ol.style.lineHeight = '1.9';

            items.forEach(text => {
                const li = document.createElement('li');
                li.textContent = text;
                ol.appendChild(li);
            });

            preview.appendChild(ol);
            wrap.style.display = 'block';
        }
    }

    resetOrderedList() {
        ['ol-title', 'ol-type', 'ol-items'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = '';
        });
        const codeEl = document.getElementById('ol-code');
        if (codeEl) codeEl.textContent = 'Your code will appear here…';
        const wrap = document.getElementById('ol-preview-wrap');
        if (wrap) wrap.style.display = 'none';
        const fb = document.getElementById('step1-feedback');
        if (fb) fb.innerHTML = '';
    }

    // =========================================================
    // ---- MCQ (shared across steps) ----
    // =========================================================
    answerMCQ(btn, qid) {
        const isCorrect = btn.dataset.correct === 'true';
        const container = btn.closest('.mcq');
        if (!container) return;
        const explain = container.querySelector('.mcq-explain');

        if (isCorrect) {
            container.querySelectorAll('.mcq-btn').forEach(b => {
                b.disabled = true;
                if (b === btn) b.classList.add('correct');
            });
            if (explain) {
                explain.textContent = btn.dataset.explain || 'Correct!';
                explain.style.color = '#9ae6b4';
            }
            this._answeredMCQs.add(qid);
            this._checkStepQuiz(qid.split('-')[0]);
        } else {
            btn.classList.add('incorrect');
            if (explain) {
                explain.textContent = 'Not quite — try again!';
                explain.style.color = '#feb2b2';
            }
        }
    }

    async _checkStepQuiz(stepId) {
        const answered = [...this._answeredMCQs].filter(q => q.startsWith(stepId + '-'));
        if (answered.length < 3) return;

        const fb = document.getElementById(stepId + '-feedback');
        const awarded = await this.awardActivityXP(
            stepId + '-quiz', 25, `${stepId} quiz`
        );

        if (stepId === 'step2') {
            this.feedback(fb, 'success',
                awarded ? 'Excellent! +25 XP' : 'Excellent!',
                'You know when to use &lt;ol&gt; and when to use &lt;ul&gt;.');
        } else if (stepId === 'step5') {
            this.feedback(fb, 'success',
                awarded ? 'Perfect! +25 XP' : 'Perfect!',
                'You understand table accessibility.');
        }
    }

    // =========================================================
    // ---- ACTIVITY 3: Nested List Checker ----
    // =========================================================
    async checkNestedList() {
        const codeEl = document.getElementById('nested-code');
        const code   = codeEl ? codeEl.value : '';

        const openOuter   = /<(ul|ol)\b[^>]*>/i.test(code);
        const liCount     = (code.match(/<li\b[^>]*>/gi) || []).length;
        const nested      = /<li\b[^>]*>[\s\S]*?<(ul|ol)\b[\s\S]*?<\/li>/i.test(code);
        const closers     = /<\/(ul|ol)>\s*$/i.test(code.trim()) ||
                            /<\/(ul|ol)>/i.test(code);

        const checks = {
            outer:  openOuter,
            lis:    liCount >= 2,
            nested: nested,
            closed: closers &&
                    (code.match(/<\/li>/gi) || []).length >= liCount,
        };

        const listItems = document.querySelectorAll('#nested-checklist li');
        const keys = ['outer', 'lis', 'nested', 'closed'];
        let passed = 0;

        keys.forEach((key, i) => {
            const li = listItems[i];
            if (!li) return;
            const ok = checks[key];
            if (ok) passed++;

            const base = li.textContent.replace(/^[⬜✅]\s*/, '');
            li.textContent = (ok ? '✅ ' : '⬜ ') + base;
            li.classList.toggle('ok', ok);
        });

        // Live preview (rendered in a sandboxed wrapper so we don't disturb our DOM)
        const wrap    = document.getElementById('nested-preview-wrap');
        const preview = document.getElementById('nested-preview');
        if (preview && passed >= 3) {
            preview.innerHTML = '';
            const sandbox = document.createElement('div');
            sandbox.style.color = '#cbd5e0';
            sandbox.style.paddingLeft = '4px';
            sandbox.style.lineHeight = '1.9';
            // Safe: user only types list markup in this exercise
            sandbox.innerHTML = code;
            preview.appendChild(sandbox);
            if (wrap) wrap.style.display = 'block';
        } else if (wrap) {
            wrap.style.display = 'none';
        }

        const fb = document.getElementById('step3-feedback');
        if (passed === 4) {
            const awarded = await this.awardActivityXP(
                'nested-list', 25, 'Nested list builder'
            );
            this.feedback(fb, 'success',
                awarded ? 'Perfect nesting! +25 XP' : 'Perfect nesting!',
                'Your inner list sits correctly inside its parent <li>.');
        } else {
            this.feedback(fb, 'hint', 'Keep going!',
                `${passed}/4 checks passed. Remember: the inner list goes INSIDE the <li>.`);
        }
    }

    resetNestedList() {
        const codeEl = document.getElementById('nested-code');
        if (codeEl) codeEl.value = '';

        document.querySelectorAll('#nested-checklist li').forEach(li => {
            const base = li.textContent.replace(/^[⬜✅]\s*/, '');
            li.textContent = '⬜ ' + base;
            li.classList.remove('ok');
        });

        const wrap = document.getElementById('nested-preview-wrap');
        if (wrap) wrap.style.display = 'none';
        const fb = document.getElementById('step3-feedback');
        if (fb) fb.innerHTML = '';
    }

    // =========================================================
    // ---- ACTIVITY 4: Table Anatomy Matching ----
    // =========================================================
    async checkTableMatch(select) {
        const isCorrect = select.value === select.dataset.correct;
        select.classList.remove('correct', 'incorrect');
        if (select.value) {
            select.classList.add(isCorrect ? 'correct' : 'incorrect');
        }
        await this._updateTableMatchFeedback();
    }

    async _updateTableMatchFeedback() {
        const selects = document.querySelectorAll('#table-match select');
        let correct = 0, filled = 0;

        selects.forEach(sel => {
            if (sel.value) {
                filled++;
                if (sel.value === sel.dataset.correct) correct++;
            }
        });

        const fb = document.getElementById('step4-feedback');
        if (filled === selects.length) {
            if (correct === selects.length) {
                const awarded = await this.awardActivityXP(
                    'table-match', 25, 'Table anatomy'
                );
                this.feedback(fb, 'success',
                    awarded ? 'Perfect! +25 XP' : 'Perfect!',
                    'You know every core table tag.');
            } else {
                this.feedback(fb, 'hint', 'Almost There!',
                    `You got ${correct}/${selects.length} correct. Try again!`);
            }
        }
    }

    // =========================================================
    // ---- PRACTICAL ASSESSMENT: 20-mark project ----
    // =========================================================
    async markProject() {
        const codeEl = document.getElementById('project-code');
        const code   = codeEl ? codeEl.value : '';
        const results = [];

        // Check 1 — Ordered list with 3+ items (5 marks)
        const olMatch = /<ol\b[^>]*>([\s\S]*?)<\/ol>/i.exec(code);
        const olItemCount = olMatch
            ? (olMatch[1].match(/<li\b[^>]*>/gi) || []).length
            : 0;
        results.push({
            label: 'Ordered list (<code>&lt;ol&gt;</code>) with 3+ items',
            pass: olItemCount >= 3,
            marks: 5,
        });

        // Check 2 — Unordered list with 3+ items (5 marks)
        const ulMatch = /<ul\b[^>]*>([\s\S]*?)<\/ul>/i.exec(code);
        const ulItemCount = ulMatch
            ? (ulMatch[1].match(/<li\b[^>]*>/gi) || []).length
            : 0;
        results.push({
            label: 'Unordered list (<code>&lt;ul&gt;</code>) with 3+ items',
            pass: ulItemCount >= 3,
            marks: 5,
        });

        // Check 3 — Table with tr + th + td (5 marks)
        const hasTable = /<table\b/i.test(code);
        const hasTr    = /<tr\b/i.test(code);
        const hasTh    = /<th\b/i.test(code);
        const hasTd    = /<td\b/i.test(code);
        results.push({
            label: 'Table with <code>&lt;tr&gt;</code>, <code>&lt;th&gt;</code> and <code>&lt;td&gt;</code>',
            pass: hasTable && hasTr && hasTh && hasTd,
            marks: 5,
        });

        // Check 4 — Caption OR scope attribute (5 marks)
        const hasCaption = /<caption\b/i.test(code);
        const hasScope   = /<th\b[^>]*\bscope\s*=\s*["'](col|row|colgroup|rowgroup)["']/i.test(code);
        results.push({
            label: '<code>&lt;caption&gt;</code> or <code>scope</code> attribute on a header',
            pass: hasCaption || hasScope,
            marks: 5,
        });

        const totalMarks = results.reduce(
            (sum, r) => sum + (r.pass ? r.marks : 0), 0
        );

        const xpReward = totalMarks >= 15 ? 50 : 0;
        const { saved, awarded } = await this.saveActivityData(
            'project',
            { code, marks: totalMarks, results },
            xpReward,
            'Practical project'
        );

        // Render results panel
        const panel = document.getElementById('project-results');
        if (panel) {
            const rows = results.map(r => `
                <tr>
                    <td>${r.pass ? '✅' : '❌'} ${r.label}</td>
                    <td>${r.pass ? r.marks : 0} / ${r.marks}</td>
                </tr>
            `).join('');

            const badge = totalMarks >= 15
                ? '<span style="color:#9ae6b4;">PASS</span>'
                : '<span style="color:#feb2b2;">Keep trying</span>';

            panel.innerHTML = `
                <div class="documentation-log" style="margin-top:20px;">
                    <h4 style="color:#f6ad55; margin-bottom:10px;">📊 Project Mark Sheet — ${badge}</h4>
                    <table class="marks-table">
                        ${rows}
                        <tr class="total">
                            <td>Total</td>
                            <td>${totalMarks} / 20</td>
                        </tr>
                    </table>
                    ${!saved ? '<p style="color:#feb2b2; font-size:0.85rem; margin-top:8px;">⚠️ Your code could not be saved to the server.</p>' : ''}
                </div>
            `;
        }

        const fb = document.getElementById('step6-feedback');
        if (totalMarks === 20) {
            this.feedback(fb, 'success',
                awarded ? '🏆 Outstanding! 20/20 +50 XP' : '🏆 Outstanding! 20/20',
                'Every requirement met. Excellent work.');
        } else if (totalMarks >= 15) {
            this.feedback(fb, 'success',
                awarded ? `Great! ${totalMarks}/20 +50 XP` : `Great! ${totalMarks}/20`,
                'A passing score. Review the checklist to reach 20.');
        } else {
            this.feedback(fb, 'hint', 'Not quite there yet',
                `You scored ${totalMarks}/20. Check the mark sheet above and try again.`);
        }
    }

    // =========================================================
    // ---- REFLECTIONS ----
    // =========================================================
    async saveReflections() {
        const data = {
            clicked:    document.getElementById('reflection-clicked')?.value    || '',
            realworld:  document.getElementById('reflection-realworld')?.value  || '',
        };

        const { saved, awarded } = await this.saveActivityData(
            'reflections', data, 25, 'Lists & tables reflections'
        );

        const fb = document.getElementById('step7-feedback');
        if (!saved) {
            this.feedback(fb, 'error', 'Could not save',
                'Something went wrong. Please try again.');
            return;
        }
        this.feedback(fb, 'success',
            awarded ? 'Reflections Saved! +25 XP' : 'Reflections Updated',
            awarded
                ? 'Great thinking — these insights will help your next build.'
                : 'Your previous reflections were updated. (XP already awarded.)');
    }

    // =========================================================
    // ---- STEP COMPLETION ----
    // =========================================================
    async completeStep(slug) {
        if (super.completeStep) {
            await super.completeStep(slug);
        }
        this._completedSteps.add(slug);
        this._updateProgress();

        const fb = document.getElementById(`${slug}-feedback`);
        if (fb && !fb.innerHTML) {
            this.feedback(fb, 'success', 'Step Complete!',
                'You have marked this step as complete.');
        }
    }

    _updateProgress() {
        const el = document.getElementById('step-progress');
        if (el) el.textContent = `${this._completedSteps.size}/7`;
    }

    // =========================================================
    // ---- RESTORE SAVED DATA ----
    // =========================================================
    _restoreData() {
        const progress = this.store?.state?.progressData || {};

        // Reflections
        const refs = progress['lists:reflections'];
        if (refs?.responseData) {
            try {
                const data = JSON.parse(refs.responseData);
                const c = document.getElementById('reflection-clicked');
                const r = document.getElementById('reflection-realworld');
                if (c) c.value = data.clicked   || '';
                if (r) r.value = data.realworld || '';
            } catch (_) {}
        }

        // Project code
        const project = progress['lists:project'];
        if (project?.responseData) {
            try {
                const data = JSON.parse(project.responseData);
                const codeEl = document.getElementById('project-code');
                if (codeEl && data.code) codeEl.value = data.code;
            } catch (_) {}
        }
    }
}

// =========================================================
// ---- BOOTSTRAP + GLOBAL BINDINGS ----
// =========================================================
const page = new ListsTablesPage();
page.start();

window.buildOrderedList = () => page.buildOrderedList();
window.resetOrderedList = () => page.resetOrderedList();
window.answerMCQ        = (btn, qid) => page.answerMCQ(btn, qid);
window.checkNestedList  = () => page.checkNestedList();
window.resetNestedList  = () => page.resetNestedList();
window.checkTableMatch  = (sel) => page.checkTableMatch(sel);
window.markProject      = () => page.markProject();
window.saveReflections  = () => page.saveReflections();
window.completeStep     = (slug) => page.completeStep(slug);

// Keep a reference for debugging
window.QuestPage = page;