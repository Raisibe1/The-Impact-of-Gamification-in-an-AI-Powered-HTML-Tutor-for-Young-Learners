import { PageShell } from './page_shell.js';
import { STEP_LESSONS } from './lesson_steps.js';

class MultimediaPage extends PageShell {
    constructor() {
        super({
            lessonSlug: 'multimedia',
            steps: STEP_LESSONS.multimedia?.steps || [],
        });
        this._dragData = null;
        this._answeredMCQs = new Set();
        this._completedSteps = new Set();
    }

    async start() {
        await super.start();
        this._bindMediaDrag();
        this._restoreData();
        this._updateProgress();
    }

    // =========================================================
    // ---- DRAG & DROP (Local vs Online media sort) ----
    // =========================================================
    _bindMediaDrag() {
        document.querySelectorAll('#media-sort .drag-item').forEach(item => {
            item.addEventListener('dragstart', () => {
                this._dragData = {
                    term: item.dataset.term,
                    category: item.dataset.category,
                    el: item,
                };
                item.classList.add('dragging');
            });
            item.addEventListener('dragend', () => {
                item.classList.remove('dragging');
            });
        });

        document.querySelectorAll('#media-sort .drop-zone').forEach(zone => {
            zone.addEventListener('dragover', e => {
                e.preventDefault();
                zone.classList.add('drag-over');
            });
            zone.addEventListener('dragleave', () =>
                zone.classList.remove('drag-over'));
            zone.addEventListener('drop', e => {
                e.preventDefault();
                zone.classList.remove('drag-over');
                if (!this._dragData) return;

                // Remove placeholder if present
                const placeholder = zone.querySelector('.placeholder');
                if (placeholder) placeholder.remove();

                // Create a chip inside the zone
                const chip = document.createElement('div');
                chip.className = 'dropped-chip';
                chip.textContent = this._dragData.term;
                chip.dataset.category = this._dragData.category;
                zone.appendChild(chip);

                // Mark the source item as used
                this._dragData.el.classList.add('used');
                this._dragData.el.setAttribute('draggable', 'false');
                this._dragData = null;
            });
        });
    }

    // =========================================================
    // ---- ACTIVITY 1: Link Builder ----
    // =========================================================
    buildLink() {
        const urlEl  = document.getElementById('lb-url');
        const textEl = document.getElementById('lb-text');
        const url    = (urlEl?.value || '').trim() || 'https://www.gov.za/';
        const text   = (textEl?.value || '').trim() || 'Visit the website';

        // Show the generated HTML as plain text
        const codeEl = document.getElementById('lb-code');
        if (codeEl) {
            codeEl.textContent =
                `<a href="${url}">\n  ${text}\n</a>`;
        }

        // Show the live preview using a real anchor element (safe)
        const wrap    = document.getElementById('lb-preview-wrap');
        const preview = document.getElementById('lb-preview');
        if (wrap && preview) {
            preview.innerHTML = '';
            const a = document.createElement('a');
            a.href = url;
            a.target = '_blank';
            a.rel = 'noopener';
            a.textContent = text;
            preview.appendChild(a);
            wrap.style.display = 'block';
        }
    }

    // =========================================================
    // ---- ACTIVITY 2: Link-type Matching ----
    // =========================================================
    async checkLinkMatch(select) {
        const isCorrect = select.value === select.dataset.correct;
        select.classList.remove('correct', 'incorrect');
        if (select.value) {
            select.classList.add(isCorrect ? 'correct' : 'incorrect');
        }
        await this._updateLinkMatchFeedback();
    }

    async _updateLinkMatchFeedback() {
        const selects = document.querySelectorAll('#link-matching select');
        let correct = 0, filled = 0;

        selects.forEach(sel => {
            if (sel.value) {
                filled++;
                if (sel.value === sel.dataset.correct) correct++;
            }
        });

        const fb = document.getElementById('step2-feedback');
        if (filled === selects.length) {
            if (correct === selects.length) {
                const awarded = await this.awardActivityXP(
                    'link-match', 25, 'Link types match'
                );
                this.feedback(fb, 'success',
                    awarded ? 'Perfect! +25 XP' : 'Perfect!',
                    "You know all five types of hyperlinks.");
            } else {
                this.feedback(fb, 'hint', 'Almost There!',
                    `You got ${correct}/${selects.length} correct. Try again!`);
            }
        }
    }

    // =========================================================
    // ---- ACTIVITY 3: Multiple Choice (File paths) ----
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
            this._checkAllMCQs();
        } else {
            btn.classList.add('incorrect');
            if (explain) {
                explain.textContent = 'Not quite — try again!';
                explain.style.color = '#feb2b2';
            }
        }
    }

    async _checkAllMCQs() {
        if (this._answeredMCQs.size < 3) return;
        const awarded = await this.awardActivityXP(
            'path-mcq', 25, 'File path quiz'
        );
        const fb = document.getElementById('step3-feedback');
        this.feedback(fb, 'success',
            awarded ? 'All paths correct! +25 XP' : 'All paths correct!',
            'You can read file paths like a pro.');
    }

    // =========================================================
    // ---- ACTIVITY 4: Video code checker ----
    // =========================================================
    async checkMediaCode() {
        const codeEl = document.getElementById('media-code');
        const code   = codeEl ? codeEl.value : '';

        const checks = {
            openTag:  /<video\b/i.test(code),
            controls: /<video\b[^>]*\bcontrols\b/i.test(code),
            source:   /<source\b[^>]*src\s*=\s*["'][^"']+["']/i.test(code) ||
                      /<video\b[^>]*src\s*=\s*["'][^"']+["']/i.test(code),
            closeTag: /<\/video>/i.test(code),
        };

        const listItems = document.querySelectorAll('#media-checklist li');
        const keys = ['openTag', 'controls', 'source', 'closeTag'];
        let passed = 0;

        keys.forEach((key, i) => {
            const li = listItems[i];
            if (!li) return;
            const isOk = checks[key];
            if (isOk) passed++;

            // Extract the base label (strip any existing ⬜ / ✅ prefix)
            const base = li.textContent.replace(/^[⬜✅]\s*/, '');
            li.textContent = (isOk ? '✅ ' : '⬜ ') + base;
            li.classList.toggle('ok', isOk);
        });

        const fb = document.getElementById('step4-feedback');
        if (passed === 4) {
            const awarded = await this.awardActivityXP(
                'media-code', 25, 'Video player code'
            );
            this.feedback(fb, 'success',
                awarded ? 'Perfect video code! +25 XP' : 'Perfect video code!',
                'You built a working video player.');
        } else {
            this.feedback(fb, 'hint', 'Keep going!',
                `${passed}/4 checks passed. Review your code and try again.`);
        }
    }

    resetMediaCode() {
        const codeEl = document.getElementById('media-code');
        if (codeEl) codeEl.value = '';

        document.querySelectorAll('#media-checklist li').forEach(li => {
            const base = li.textContent.replace(/^[⬜✅]\s*/, '');
            li.textContent = '⬜ ' + base;
            li.classList.remove('ok');
        });

        const fb = document.getElementById('step4-feedback');
        if (fb) fb.innerHTML = '';
    }

    // =========================================================
    // ---- ACTIVITY 5: Media-source Sort ----
    // =========================================================
    async checkMediaSource() {
        const allItems  = document.querySelectorAll('#media-sort .drag-item');
        const usedItems = document.querySelectorAll('#media-sort .drag-item.used');
        const fb = document.getElementById('step5-feedback');

        if (usedItems.length < allItems.length) {
            this.feedback(fb, 'hint', 'Not finished yet',
                `Drop all ${allItems.length} items into a bucket first.`);
            return;
        }

        const zones = document.querySelectorAll('#media-sort .drop-zone');
        let correct = 0, total = 0;

        zones.forEach(zone => {
            const expected = zone.dataset.expected;
            zone.querySelectorAll('.dropped-chip').forEach(chip => {
                total++;
                if (chip.dataset.category === expected) {
                    chip.classList.add('correct');
                    chip.classList.remove('incorrect');
                    correct++;
                } else {
                    chip.classList.add('incorrect');
                    chip.classList.remove('correct');
                }
            });
        });

        if (correct === total) {
            const awarded = await this.awardActivityXP(
                'media-source', 25, 'Local vs online media'
            );
            this.feedback(fb, 'success',
                awarded ? 'Perfect sorting! +25 XP' : 'Perfect sorting!',
                'You can tell local files from online media.');
        } else {
            this.feedback(fb, 'hint', 'Almost there!',
                `You got ${correct}/${total} correct. Try again.`);
        }
    }

    resetMediaSource() {
        const container = document.getElementById('media-sort');
        if (!container) return;

        // Clear chips and restore placeholders
        container.querySelectorAll('.drop-zone').forEach(zone => {
            zone.innerHTML = '';
            const placeholder = document.createElement('span');
            placeholder.className = 'placeholder';
            placeholder.textContent = zone.dataset.expected === 'local'
                ? 'Drop local files here'
                : 'Drop online media here';
            zone.appendChild(placeholder);
        });

        // Re-enable all drag items
        container.querySelectorAll('.drag-item').forEach(item => {
            item.classList.remove('used', 'dragging');
            item.setAttribute('draggable', 'true');
        });

        const fb = document.getElementById('step5-feedback');
        if (fb) fb.innerHTML = '';
    }

    // =========================================================
    // ---- PRACTICAL ASSESSMENT: 20-mark project ----
    // =========================================================
    async markProject() {
        const codeEl = document.getElementById('project-code');
        const code   = codeEl ? codeEl.value : '';
        const results = [];

        // Check 1 — Hyperlink with href (5 marks)
        const hasLink = /<a\s+[^>]*href\s*=\s*["'][^"']+["'][^>]*>/i.test(code);
        results.push({ label: 'Hyperlink with <code>href</code>', pass: hasLink, marks: 5 });

        // Check 2 — Image with src + alt (5 marks)
        const imgTag = /<img\b[^>]*>/i.exec(code);
        const imgTagStr = imgTag ? imgTag[0] : '';
        const imgPass = imgTag &&
            /\bsrc\s*=\s*["'][^"']+["']/i.test(imgTagStr) &&
            /\balt\s*=\s*["'][^"']+["']/i.test(imgTagStr);
        results.push({ label: 'Image with <code>src</code> and <code>alt</code>', pass: !!imgPass, marks: 5 });

        // Check 3 — Audio or video with controls (5 marks)
        const mediaTag = /<(audio|video)\b[^>]*>/i.exec(code);
        const mediaPass = mediaTag && /\bcontrols\b/i.test(mediaTag[0]);
        results.push({ label: 'Media player with <code>controls</code>', pass: !!mediaPass, marks: 5 });

        // Check 4 — Same-page link with matching id (5 marks)
        const hashMatch = /href\s*=\s*["']#([\w-]+)["']/i.exec(code);
        const samePagePass = hashMatch &&
            new RegExp(`\\bid\\s*=\\s*["']${hashMatch[1]}["']`, 'i').test(code);
        results.push({
            label: 'Same-page link (<code>#id</code>) with matching <code>id</code>',
            pass: !!samePagePass,
            marks: 5,
        });

        const totalMarks = results.reduce(
            (sum, r) => sum + (r.pass ? r.marks : 0), 0
        );

        // Save attempt + award XP based on performance
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
            surprise: document.getElementById('reflection-surprise')?.value || '',
            next:     document.getElementById('reflection-next')?.value || '',
        };

        const { saved, awarded } = await this.saveActivityData(
            'reflections', data, 25, 'Links & media reflections'
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
        const refs = progress['multimedia:reflections'];
        if (refs?.responseData) {
            try {
                const data = JSON.parse(refs.responseData);
                const s = document.getElementById('reflection-surprise');
                const n = document.getElementById('reflection-next');
                if (s) s.value = data.surprise || '';
                if (n) n.value = data.next || '';
            } catch (_) {}
        }

        // Project code
        const project = progress['multimedia:project'];
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
const page = new MultimediaPage();
page.start();

window.buildLink        = () => page.buildLink();
window.checkLinkMatch   = (sel) => page.checkLinkMatch(sel);
window.answerMCQ        = (btn, qid) => page.answerMCQ(btn, qid);
window.checkMediaCode   = () => page.checkMediaCode();
window.resetMediaCode   = () => page.resetMediaCode();
window.checkMediaSource = () => page.checkMediaSource();
window.resetMediaSource = () => page.resetMediaSource();
window.markProject      = () => page.markProject();
window.saveReflections  = () => page.saveReflections();
window.completeStep     = (slug) => page.completeStep(slug);

// Keep a reference for debugging
window.QuestPage = page;