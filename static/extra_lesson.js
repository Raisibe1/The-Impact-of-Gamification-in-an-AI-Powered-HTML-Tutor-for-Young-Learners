export const HTML_LESSON_ORDER = [
    'html',
    'html-links',
    'html-media',
    'html-lists',
    'html-forms',
    'html-semantics',
];

/* ---------- tiny validator helpers ---------- */
const stripComments = (code) => code.replace(/<!--[\s\S]*?-->/g, '');
const count = (code, re) => (code.match(re) || []).length;
const has   = (code, re) => re.test(code);

/* ---------- badges ---------- */
export const HTML_BADGES = {
    'html':           { name: 'Structure Scout',  description: 'You can build a valid HTML skeleton from scratch.' },
    'html-links':     { name: 'Portal Master',    description: 'You built working portals between pages.' },
    'html-media':     { name: 'Media Mogul',      description: 'Images, audio, video and embeds — all under control.' },
    'html-lists':     { name: 'Data Dragon',      description: 'You organised raw data into lists and tables.' },
    'html-forms':     { name: 'Input Wizard',     description: 'You built an accessible, labelled form.' },
    'html-semantics': { name: 'Semantics Sage',   description: 'Your pages now speak the browser’s language.' },
};

/* ---------- lessons ---------- */
export const HTML_LESSONS = {

/* =========================================================
   LEVEL 1 — HTML Foundations
   ========================================================= */
'html': {
    id: 'first-page',
    title: 'HTML Foundations',
    badge: '🧱',
    xp: 40,
    concept: `
        <p>HTML is the <strong>skeleton</strong> of every web page. It does not make things pretty —
        it tells the browser what each piece of content <em>is</em>: a heading, a paragraph, a link, a list.</p>

        <h4>The five tags you will use forever</h4>
        <ul>
            <li><code>&lt;h1&gt;</code> … <code>&lt;h6&gt;</code> — headings, biggest to smallest</li>
            <li><code>&lt;p&gt;</code> — a paragraph of text</li>
            <li><code>&lt;strong&gt;</code> / <code>&lt;em&gt;</code> — importance / emphasis (not just "bold")</li>
            <li><code>&lt;br&gt;</code> / <code>&lt;hr&gt;</code> — a line break / a thematic divider (no closing tag)</li>
            <li><code>&lt;!-- comment --&gt;</code> — notes for humans, ignored by the browser</li>
        </ul>

        <h4>The skeleton every page needs</h4>
<pre>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
  &lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;Page name (shows in the tab)&lt;/title&gt;
  &lt;/head&gt;
  &lt;body&gt;
    &lt;h1&gt;Hello, world&lt;/h1&gt;
  &lt;/body&gt;
&lt;/html&gt;</pre>

        <h4>Nesting rules that save your life</h4>
        <ul>
            <li>Close every tag you open, in the <strong>reverse order</strong> you opened them.</li>
            <li>Only <strong>one</strong> <code>&lt;h1&gt;</code> per page — it is the page’s title.</li>
            <li>Never skip heading levels (<code>h2</code> → <code>h4</code> confuses screen readers).</li>
            <li><code>lang="en"</code> tells screen readers which voice to use.</li>
        </ul>
    `,
    visual: {
        type: 'html',
        html: `
            <div style="font-family:system-ui,sans-serif;padding:18px;line-height:1.55;color:#1f2933;">
                <h1 style="font-size:1.5rem;margin:0 0 4px;">The Hero's Journey</h1>
                <h2 style="font-size:1.05rem;margin:0 0 8px;color:#52606d;">Chapter One</h2>
                <p style="margin:0 0 8px;">Every page starts with a <strong>heading</strong> and a paragraph.</p>
                <p style="margin:0 0 8px;">Use <em>emphasis</em> for the words that <mark>really matter</mark>.</p>
                <hr style="border:none;border-top:1px solid #d9e2ec;margin:12px 0;">
                <p style="margin:0;font-size:.82rem;color:#7b8794;">
                    Headings build an outline. Screen readers jump between them.
                </p>
            </div>
        `,
    },
    challenge: {
        title: 'Challenge: Build Your First Page',
        description:
            'Fill in the body so the page has exactly one <h1>, at least two paragraphs, and one <strong> or <em> inside the text. Keep the doctype, the lang attribute, the meta charset and the title.',
        starterCode:
`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>My First Page</title>
</head>
<body>

  <!-- 1. Add an <h1> title -->

  <!-- 2. Add two paragraphs -->

  <!-- 3. Make one word <strong> or <em> -->

</body>
</html>`,
        hint:
`Your body should look something like this:

<h1>My First Page</h1>
<p>I am learning <strong>HTML</strong>.</p>
<p>This is my second paragraph.</p>

Make sure the <h1> and both <p> tags are closed.`,
        xp: 40,
        slug: 'first-page',
        test: (raw) => {
            const code = stripComments(raw);
            return has(code, /<!doctype\s+html/i)
                && has(code, /<html[^>]*\slang\s*=\s*["'][a-z-]+["']/i)
                && has(code, /<head[\s>]/i)
                && has(code, /<title>\s*[^<\s][^<]*<\/title>/i)
                && has(code, /<meta[^>]*charset/i)
                && has(code, /<body[\s>]/i)
                && has(code, /<\/body>/i)
                && count(code, /<h1[\s>]/gi) === 1
                && count(code, /<\/h1>/gi) >= 1
                && count(code, /<p[\s>]/gi) >= 2
                && count(code, /<\/p>/gi) >= 2
                && has(code, /<(strong|em)[\s>]/i);
        },
    },
    nextLesson: 'html-links',
},

/* =========================================================
   LEVEL 2 — Portal Maker (Links)
   ========================================================= */
'html-links': {
    id: 'html-links',
    title: 'Portal Maker',
    badge: '🔗',
    xp: 50,
    concept: `
        <p>The internet is a huge map, and links are the <strong>portals</strong> between places.
        A portal is built with the anchor tag:</p>
<pre>&lt;a href="https://www.wikipedia.org"&gt;Visit Wikipedia&lt;/a&gt;</pre>
        <ul>
            <li><code>&lt;a&gt;</code> is the portal.</li>
            <li><code>href</code> is where the portal <em>leads</em>.</li>
            <li>The text in the middle is what players <em>click</em>.</li>
        </ul>

        <h4>Portal types</h4>
        <table>
            <thead>
                <tr><th>Portal</th><th>Example</th><th>Use it for</th></tr>
            </thead>
            <tbody>
                <tr><td>Absolute</td><td><code>href="https://example.com/page"</code></td><td>Other websites</td></tr>
                <tr><td>Relative</td><td><code>href="about.html"</code></td><td>Other pages on your own site</td></tr>
                <tr><td>Same-page</td><td><code>href="#cheats"</code></td><td>Jumping to a section</td></tr>
                <tr><td>Email</td><td><code>href="mailto:me@example.com"</code></td><td>Opens an email app</td></tr>
                <tr><td>Phone</td><td><code>href="tel:+27123456789"</code></td><td>Calls on mobile</td></tr>
            </tbody>
        </table>

        <h4>Open in a new tab</h4>
<pre>&lt;a href="https://example.com" target="_blank" rel="noopener"&gt;Open me&lt;/a&gt;</pre>
        <p><code>rel="noopener"</code> stops the new tab from taking control of your page. Always pair it with
        <code>target="_blank"</code>.</p>

        <h4>Good vs bad link text</h4>
        <ul>
            <li>❌ <em>"Click here"</em> — meaningless out of context, and useless to screen-reader users.</li>
            <li>✅ <em>"Download the level 2 cheat sheet"</em> — describes the destination.</li>
        </ul>
        <p>A same-page link only works if the target element has a matching <code>id</code>:
        <code>&lt;h2 id="contact"&gt;</code>.</p>
    `,
    visual: {
        type: 'html',
        html: `
            <div style="font-family:system-ui,sans-serif;padding:18px;line-height:1.6;color:#1f2933;">
                <p style="margin:0 0 12px;font-weight:600;">Every link is a portal 🌀</p>
                <div style="border:1px solid #d9e2ec;border-radius:8px;padding:10px 14px;margin-bottom:10px;">
                    <div style="font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:#7b8794;">Absolute</div>
                    <span style="color:#2563eb;text-decoration:underline;">https://wikipedia.org</span>
                    <div style="font-size:.8rem;color:#616e7c;">Leaves your site entirely</div>
                </div>
                <div style="border:1px solid #d9e2ec;border-radius:8px;padding:10px 14px;margin-bottom:10px;">
                    <div style="font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:#7b8794;">Relative</div>
                    <span style="color:#2563eb;text-decoration:underline;">about.html</span>
                    <div style="font-size:.8rem;color:#616e7c;">Stays inside your own folder</div>
                </div>
                <div style="border:1px solid #d9e2ec;border-radius:8px;padding:10px 14px;margin-bottom:10px;">
                    <div style="font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:#7b8794;">Same-page</div>
                    <span style="color:#2563eb;text-decoration:underline;">#contact</span>
                    <div style="font-size:.8rem;color:#616e7c;">Jumps to <code style="background:#eef2f7;padding:1px 4px;border-radius:3px;">id="contact"</code></div>
                </div>
                <div style="border:1px solid #d9e2ec;border-radius:8px;padding:10px 14px;">
                    <div style="font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:#7b8794;">New tab</div>
                    <span style="color:#2563eb;text-decoration:underline;">target="_blank"</span> +
                    <span style="color:#2563eb;text-decoration:underline;">rel="noopener"</span>
                </div>
            </div>
        `,
    },
    challenge: {
        title: 'Boss Challenge: The Link Hub',
        description:
            'Build a "My Hub" page containing: three external http(s) links, at least one of them opening in a new tab with rel="noopener"; a same-page link to #contact; a section with id="contact"; and a mailto: link inside it. No "click here" anywhere.',
        starterCode:
`<h1>My Hub</h1>

<!-- 1. Add 3 external links (one with target="_blank" rel="noopener") -->


<!-- 2. Add a same-page link that jumps to the Contact section -->


<h2 id="contact">Contact</h2>
<p>Email me:</p>
<!-- 3. Add a mailto: link here -->
`,
        hint:
`Remember the shape of a portal:

<a href="https://example.com" target="_blank" rel="noopener">Example</a>
<a href="#contact">Jump to contact</a>
<a href="mailto:me@example.com">Email me</a>

Check: do all three live inside quotes? Is #contact spelled exactly the same as the id?`,
        xp: 50,
        slug: 'html-links',
        test: (raw) => {
            const code = stripComments(raw);
            const anchors = code.match(/<a\s[^>]*>/gi) || [];
            const external = anchors.filter((a) => /href\s*=\s*["']https?:\/\//i.test(a));
            const newTab   = anchors.filter((a) =>
                /target\s*=\s*["']_blank["']/i.test(a) &&
                /rel\s*=\s*["'][^"']*noopener/i.test(a));
            return external.length >= 3
                && newTab.length >= 1
                && has(code, /href\s*=\s*["']#contact["']/i)
                && has(code, /id\s*=\s*["']contact["']/i)
                && has(code, /href\s*=\s*["']mailto:[^"']+@[^"']+["']/i)
                && !/click here/i.test(code);
        },
    },
    nextLesson: 'html-media',
},

/* =========================================================
   LEVEL 3 — Media Lab
   ========================================================= */
'html-media': {
    id: 'html-media',
    title: 'Media Lab',
    badge: '🖼️',
    xp: 50,
    concept: `
        <p>Your pages are plain and grey. Time to add colour, sound and motion.</p>

        <h4>Images</h4>
<pre>&lt;img src="cat.jpg" alt="A grey cat sleeping on a keyboard" width="400"&gt;</pre>
        <ul>
            <li><code>src</code> — where the image file lives.</li>
            <li><code>alt</code> — a description for screen readers and for when the image fails to load.</li>
            <li><code>width</code> / <code>height</code> — stops the page from jumping while it loads.</li>
            <li><code>&lt;img&gt;</code> has <strong>no closing tag</strong>.</li>
        </ul>
        <br><br><br>
        <h4>Pick the right format</h4>
        <table>
            <thead><tr><th>Format</th><th>Best for</th></tr></thead>
            <tbody>
                <tr><td>JPG</td><td>Photos</td></tr>
                <tr><td>PNG</td><td>Graphics needing transparency</td></tr>
                <tr><td>GIF</td><td>Short simple animations</td></tr>
                <tr><td>SVG</td><td>Logos and icons (never blurry)</td></tr>
                <tr><td>WebP</td><td>Small file size, good for everything</td></tr>
            </tbody>
        </table>
        <br><br><br>
        <h4>Image with a caption</h4>
<pre>&lt;figure&gt;
  &lt;img src="robot.png" alt="Blue robot waving"&gt;
  &lt;figcaption&gt;Meet Bolt, our mascot.&lt;/figcaption&gt;
&lt;/figure&gt;</pre><br><br><br>

        <h4>Audio</h4>
<pre>&lt;audio controls src="theme.mp3"&gt;&lt;/audio&gt;</pre>

       <br><br><br> <h4>Video</h4>
<pre>&lt;video controls width="500" poster="thumbnail.jpg"&gt;
  &lt;source src="trailer.mp4" type="video/mp4"&gt;
  Your browser doesn't support video.
&lt;/video&gt;</pre>
<br><br><br>
        <h4>Embedding (YouTube and friends)</h4>
<pre>&lt;iframe src="https://www.youtube.com/embed/VIDEO_ID"
        width="560" height="315"
        title="Game trailer" allowfullscreen&gt;&lt;/iframe&gt;</pre>
<br><br><br>
        <h4>Pro tips</h4>
        <ul>
            <li><code>loading="lazy"</code> delays loading until the image is scrolled into view.</li>
            <li><code>img { max-width: 100% }</code> in CSS keeps images inside phone screens.</li>
            <li>Autoplaying sound annoys people. Always use <code>controls</code>.</li>
            <li>A purely decorative image gets an <strong>empty</strong> alt: <code>alt=""</code>.</li>
        </ul>
    `,
    visual: {
        type: 'html',
        html: `
            <div style="font-family:system-ui,sans-serif;padding:18px;line-height:1.55;color:#1f2933;">
                <figure style="margin:0 0 14px;text-align:center;">
                    <svg width="140" height="90" viewBox="0 0 140 90" role="img" aria-label="Blue robot waving">
                        <rect x="35" y="15" width="70" height="55" rx="10" fill="#7fb3ff"/>
                        <circle cx="56" cy="38" r="7" fill="#0b2545"/>
                        <circle cx="84" cy="38" r="7" fill="#0b2545"/>
                        <rect x="55" y="52" width="30" height="6" rx="3" fill="#0b2545"/>
                        <rect x="20" y="30" width="12" height="30" rx="6" fill="#a9c8ff"/>
                        <rect x="108" y="30" width="12" height="30" rx="6" fill="#a9c8ff"/>
                    </svg>
                    <figcaption style="font-size:.82rem;color:#616e7c;">Meet Bolt, our mascot.</figcaption>
                </figure>
                <div style="display:flex;align-items:center;gap:10px;border:1px solid #d9e2ec;border-radius:20px;padding:8px 14px;margin-bottom:10px;">
                    <span style="font-size:1.1rem;">▶️</span>
                    <div style="flex:1;height:6px;background:#e4ebf3;border-radius:3px;"></div>
                    <span style="font-size:.75rem;color:#7b8794;">0:00 / 0:32</span>
                </div>
                <div style="position:relative;border-radius:8px;overflow:hidden;border:1px solid #d9e2ec;height:110px;background:linear-gradient(135deg,#dbeafe,#f0f9ff);display:flex;align-items:center;justify-content:center;">
                    <span style="font-size:2rem;">▶</span>
                    <span style="position:absolute;bottom:8px;left:10px;font-size:.72rem;color:#52606d;">&lt;iframe&gt; embed</span>
                </div>
            </div>
        `,
    },
   challenge: {
        title: 'Boss Challenge: The Media Showcase',
        description:
            'Build a "My Favourite Things" page with: one &lt;img&gt; that has both src and a non-empty alt, wrapped in a &lt;figure&gt; with a &lt;figcaption&gt;; one &lt;audio&gt; or &lt;video&gt; that has controls and a closing tag; and one &lt;iframe&gt; pointing at an https URL.',
        starterCode:
            `<h1>My Favourite Things</h1>

            <!-- 1. A <figure> with an <img> (src + alt) and a <figcaption> -->


            <!-- 2. An <audio> or <video> with controls -->


            <!-- 3. An <iframe> embedding an https URL -->
            `,
        hint:
            `Three boxes to tick:

            <figure>
              <img src="robot.png" alt="Blue robot waving">
              <figcaption>Meet Bolt.</figcaption>
            </figure>

            <audio controls src="theme.mp3"></audio>

            <iframe src="https://www.example.com" title="Trailer"></iframe>

            Remember: img has no closing tag, but audio, video and iframe do.`,
        xp: 50,
        slug: 'media-showcase',
        test: (raw) => {
            const code = stripComments(raw);
            const imgs = code.match(/<img\s[^>]*>/gi) || [];
            const goodImg = imgs.some((tag) =>
                /src\s*=\s*["'][^"']+["']/i.test(tag) &&
                /alt\s*=\s*["'][^"']+["']/i.test(tag));
            return goodImg
                && has(code, /<figure[\s>]/i)
                && has(code, /<\/figure>/i)
                && has(code, /<figcaption[^>]*>[\s\S]*?<\/figcaption>/i)
                && has(code, /<(audio|video)[^>]*\bcontrols/i)
                && (has(code, /<\/audio>/i) || has(code, /<\/video>/i))
                && has(code, /<iframe[^>]*src\s*=\s*["']https?:\/\//i)
                && has(code, /<\/iframe>/i);
        },
    },
    nextLesson: 'html-lists',
},

/* =========================================================
   LEVEL 4 — Data Vault (Lists & Tables)
   ========================================================= */
'html-lists': {
    id: 'html-lists',
    title: 'Data Vault',
    badge: '📊',
    xp: 50,
    concept: `
        <p>Information is scattered everywhere. Organise it before the vault locks.</p>

        <h4>Unordered list — order doesn't matter</h4>
<pre>&lt;ul&gt;
  &lt;li&gt;Sword&lt;/li&gt;
  &lt;li&gt;Shield&lt;/li&gt;
  &lt;li&gt;Potion&lt;/li&gt;
&lt;/ul&gt;</pre>

        <h4>Ordered list — order matters</h4>
<pre>&lt;ol&gt;
  &lt;li&gt;Open the door&lt;/li&gt;
  &lt;li&gt;Grab the key&lt;/li&gt;
  &lt;li&gt;Escape&lt;/li&gt;
&lt;/ol&gt;</pre>

        <h4>Nested list</h4>
<pre>&lt;ul&gt;
  &lt;li&gt;Weapons
    &lt;ul&gt;
      &lt;li&gt;Sword&lt;/li&gt;
      &lt;li&gt;Bow&lt;/li&gt;
    &lt;/ul&gt;
  &lt;/li&gt;
&lt;/ul&gt;</pre>
        <p>Only <code>&lt;li&gt;</code> may sit directly inside <code>&lt;ul&gt;</code> or <code>&lt;ol&gt;</code>.
        A nested list goes <strong>inside</strong> an <code>&lt;li&gt;</code>, never between items.</p>

        <h4>Description list — terms and meanings</h4>
<pre>&lt;dl&gt;
  &lt;dt&gt;HTML&lt;/dt&gt;
  &lt;dd&gt;The structure of a web page&lt;/dd&gt;
&lt;/dl&gt;</pre>

        <h4>Tables</h4>
<pre>&lt;table&gt;
  &lt;caption&gt;Top Players&lt;/caption&gt;
  &lt;thead&gt;
    &lt;tr&gt;&lt;th&gt;Name&lt;/th&gt;&lt;th&gt;Score&lt;/th&gt;&lt;/tr&gt;
  &lt;/thead&gt;
  &lt;tbody&gt;
    &lt;tr&gt;&lt;td&gt;Ava&lt;/td&gt;&lt;td&gt;980&lt;/td&gt;&lt;/tr&gt;
    &lt;tr&gt;&lt;td&gt;Leo&lt;/td&gt;&lt;td&gt;870&lt;/td&gt;&lt;/tr&gt;
  &lt;/tbody&gt;
&lt;/table&gt;</pre>

        <table>
            <thead><tr><th>Tag</th><th>Job</th></tr></thead>
            <tbody>
                <tr><td><code>&lt;table&gt;</code></td><td>The whole grid</td></tr>
                <tr><td><code>&lt;tr&gt;</code></td><td>A row</td></tr>
                <tr><td><code>&lt;th&gt;</code></td><td>A header cell (bold, helps screen readers)</td></tr>
                <tr><td><code>&lt;td&gt;</code></td><td>A normal cell</td></tr>
                <tr><td><code>&lt;thead&gt;</code> / <code>&lt;tbody&gt;</code></td><td>Groups header rows and body rows</td></tr>
                <tr><td><code>&lt;caption&gt;</code></td><td>The table's title</td></tr>
            </tbody>
        </table>

        <p><strong>Merging cells:</strong> <code>colspan="2"</code> stretches a cell across 2 columns,
        <code>rowspan="2"</code> across 2 rows.</p>
        <p><strong>Rule of thumb:</strong> tables are for <em>data</em> (scores, schedules, prices).
        Never use them to lay out a page.</p>
    `,
    visual: {
        type: 'html',
        html: `
            <div style="font-family:system-ui,sans-serif;padding:18px;line-height:1.5;color:#1f2933;">
                <table style="width:100%;border-collapse:collapse;font-size:.85rem;margin-bottom:14px;">
                    <caption style="text-align:left;font-weight:600;padding-bottom:6px;">Top Players</caption>
                    <thead>
                        <tr style="background:#eef2f7;">
                            <th style="text-align:left;padding:6px 8px;">Rank</th>
                            <th style="text-align:left;padding:6px 8px;">Name</th>
                            <th style="text-align:right;padding:6px 8px;">Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td style="padding:6px 8px;">1</td><td style="padding:6px 8px;">Ava</td><td style="padding:6px 8px;text-align:right;">980</td></tr>
                        <tr style="background:#f7f9fc;"><td style="padding:6px 8px;">2</td><td style="padding:6px 8px;">Leo</td><td style="padding:6px 8px;text-align:right;">870</td></tr>
                        <tr><td colspan="3" style="padding:6px 8px;font-style:italic;color:#616e7c;">Season 1</td></tr>
                    </tbody>
                </table>
                <div style="font-size:.85rem;">
                    <strong>Prizes</strong>
                    <ul style="margin:6px 0 0 18px;padding:0;">
                        <li>1st place
                            <ul style="margin:4px 0 0 16px;padding:0;color:#52606d;">
                                <li>Golden keyboard</li>
                                <li>500 XP</li>
                            </ul>
                        </li>
                        <li>2nd place — Silver mouse</li>
                        <li>3rd place — Bronze badge</li>
                    </ul>
                </div>
            </div>
        `,
    },
    challenge: {
        title: 'Boss Challenge: The Leaderboard',
        description:
    'Build a leaderboard page with: a &lt;table&gt; containing a &lt;caption&gt;, a &lt;thead&gt; with &lt;th&gt; cells, and at least 4 player rows (Rank / Name / Score); one cell using colspan; and below the table a "Prizes" list that is nested (a &lt;ul&gt; inside a &lt;li&gt;) with sub-items for 1st, 2nd and 3rd place.',
        starterCode:
`<h1>Game Leaderboard</h1>

<!-- 1. Table: caption, thead with <th>, 4 players, one colspan cell -->


<!-- 2. A nested list of Prizes (1st / 2nd / 3rd with sub-items) -->
`,
        hint:
`A table with a merged footer row looks like this:

<table>
  <caption>Top Players</caption>
  <thead>
    <tr><th>Rank</th><th>Name</th><th>Score</th></tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>Ava</td><td>980</td></tr>
    ...
    <tr><td colspan="3">Season 1</td></tr>
  </tbody>
</table>

For the nested list, the inner <ul> must sit INSIDE an <li>, not after it.`,
        xp: 50,
        slug: 'leaderboard',
        test: (raw) => {
            const code = stripComments(raw);
            const rows  = count(code, /<tr[\s>]/gi);
            const cells = count(code, /<t[hd][\s>]/gi);
            const uls   = count(code, /<ul[\s>]/gi);
            return has(code, /<table[\s>]/i)
                && has(code, /<\/table>/i)
                && has(code, /<caption[^>]*>\s*[^<\s][^<]*<\/caption>/i)
                && has(code, /<thead[\s>]/i)
                && has(code, /<th[\s>]/i)
                && rows >= 5
                && cells >= 13
                && has(code, /colspan\s*=\s*["']?[2-9]/i)
                && uls >= 2
                && has(code, /<li[\s>]/i);
        },
    },
    nextLesson: 'html-forms',
},

/* =========================================================
   LEVEL 5 — Form Forge
   ========================================================= */
'html-forms': {
    id: 'html-forms',
    title: 'Form Forge',
    badge: '📝',
    xp: 50,
    concept: `
        <p>Forms are how the web <strong>listens</strong>. Login boxes, search bars, sign-up pages —
        all of them are forms.</p>

        <h4>The shell</h4>
<pre>&lt;form action="/signup" method="post"&gt;
  ...
&lt;/form&gt;</pre>
        <ul>
            <li><code>action</code> — where the data is sent.</li>
            <li><code>method</code> — <code>get</code> (data in the URL) or <code>post</code> (data in the body).</li>
            <li><code>name</code> on every field — without it, the field's value is <em>never sent</em>.</li>
        </ul>

        <h4>Labels are not optional</h4>
<pre>&lt;label for="email"&gt;Email&lt;/label&gt;
&lt;input id="email" name="email" type="email" required&gt;</pre>
        <p>The <code>for</code> attribute must match the input's <code>id</code>. Clicking the label then
        focuses the input, and screen readers announce the two together. A placeholder is
        <strong>not</strong> a label.</p>

        <h4>Useful input types</h4>
        <table>
            <thead><tr><th>type</th><th>What it gives you</th></tr></thead>
            <tbody>
                <tr><td><code>text</code></td><td>Single line of text</td></tr>
                <tr><td><code>email</code></td><td>Email keyboard + built-in validation</td></tr>
                <tr><td><code>password</code></td><td>Dots instead of characters</td></tr>
                <tr><td><code>number</code></td><td>Spinner, min / max</td></tr>
                <tr><td><code>date</code></td><td>Native date picker</td></tr>
                <tr><td><code>checkbox</code> / <code>radio</code></td><td>Multiple / single choice</td></tr>
                <tr><td><code>file</code></td><td>File upload</td></tr>
            </tbody>
        </table>

        <h4>Dropdowns, big text boxes, buttons</h4>
<pre>&lt;select id="class" name="class"&gt;
  &lt;option value="mage"&gt;Mage&lt;/option&gt;
  &lt;option value="rogue"&gt;Rogue&lt;/option&gt;
&lt;/select&gt;

&lt;textarea id="bio" name="bio" rows="4"&gt;&lt;/textarea&gt;

&lt;button type="submit"&gt;Join&lt;/button&gt;</pre>

        <h4>Grouping and validation</h4>
        <ul>
            <li><code>&lt;fieldset&gt;</code> + <code>&lt;legend&gt;</code> group related fields (great for radio buttons).</li>
            <li><code>required</code> blocks submission until filled.</li>
            <li><code>minlength</code>, <code>maxlength</code>, <code>pattern</code> add extra rules.</li>
            <li>A <code>&lt;button&gt;</code> inside a form defaults to <code>type="submit"</code>.</li>
        </ul>
    `,
    visual: {
        type: 'html',
        html: `
            <div style="font-family:system-ui,sans-serif;padding:18px;color:#1f2933;font-size:.88rem;">
                <div style="margin-bottom:12px;">
                    <label style="display:block;font-weight:600;margin-bottom:4px;">Hero name</label>
                    <div style="border:1px solid #cbd2d9;border-radius:6px;padding:8px 10px;color:#9aa5b1;">e.g. Nova</div>
                </div>
                <div style="margin-bottom:12px;">
                    <label style="display:block;font-weight:600;margin-bottom:4px;">Email</label>
                    <div style="border:1px solid #cbd2d9;border-radius:6px;padding:8px 10px;color:#9aa5b1;">you@example.com</div>
                    <div style="font-size:.75rem;color:#7b8794;margin-top:4px;">type="email" · required</div>
                </div>
                <div style="margin-bottom:12px;">
                    <label style="display:block;font-weight:600;margin-bottom:4px;">Class</label>
                    <div style="border:1px solid #cbd2d9;border-radius:6px;padding:8px 10px;display:flex;justify-content:space-between;">
                        <span>Mage</span><span style="color:#9aa5b1;">▾</span>
                    </div>
                </div>
                <div style="margin-bottom:12px;">
                    <label style="display:block;font-weight:600;margin-bottom:4px;">Bio</label>
                    <div style="border:1px solid #cbd2d9;border-radius:6px;padding:8px 10px;height:56px;color:#9aa5b1;">&lt;textarea&gt;</div>
                </div>
                <div style="background:#2563eb;color:#fff;border-radius:6px;padding:9px;text-align:center;font-weight:600;">Join the Guild</div>
            </div>
        `,
    },
    challenge: {
        title: 'Boss Challenge: Join the Guild',
        description:
    'Build a sign-up form inside a <code>&lt;form&gt;</code> element with: a <code>&lt;label for="name"&gt;</code> paired with an <code>&lt;input id="name"&gt;</code>; an <code>&lt;input type="email"&gt;</code> with required; a <code>&lt;select&gt;</code> with at least 3 <code>&lt;option&gt;</code>s; a <code>&lt;textarea&gt;</code> with a closing tag; and a submit button. Every field needs a name attribute.',
        starterCode:
`<h1>Join the Guild</h1>

<form action="/signup" method="post">

  <!-- 1. label + input for the hero name (for / id must match) -->

  <!-- 2. email input with required -->

  <!-- 3. select with 3 options -->

  <!-- 4. textarea -->

  <!-- 5. submit button -->

</form>
`,
        hint:
`The label/input pair is the heart of it:

<label for="name">Hero name</label>
<input id="name" name="name" type="text" required>

Then:
<select id="class" name="class">
  <option value="mage">Mage</option>
  <option value="rogue">Rogue</option>
  <option value="healer">Healer</option>
</select>

<textarea id="bio" name="bio"></textarea>
<button type="submit">Join</button>

Do the for and id values match exactly?`,
        xp: 50,
        slug: 'guild-form',
        test: (raw) => {
            const code = stripComments(raw);
            const options = count(code, /<option[\s>]/gi);
            return has(code, /<form[\s>]/i)
                && has(code, /<\/form>/i)
                && has(code, /<label[^>]*\bfor\s*=\s*["']name["']/i)
                && has(code, /<input[^>]*\bid\s*=\s*["']name["']/i)
                && has(code, /<input[^>]*type\s*=\s*["']email["']/i)
                && has(code, /\brequired\b/i)
                && has(code, /<select[\s>]/i)
                && options >= 3
                && has(code, /<textarea[\s>]/i)
                && has(code, /<\/textarea>/i)
                && has(code, /(type\s*=\s*["']submit["']|<button[\s>])/i);
        },
    },
    nextLesson: 'html-semantics',
},

/* =========================================================
   LEVEL 6 — Structure Sanctum (Semantic HTML)
   ========================================================= */
'html-semantics': {
    id: 'html-semantics',
    title: 'Structure Sanctum',
    badge: '🏛️',
    xp: 60,
    concept: `
        <p>You can build a whole page out of <code>&lt;div&gt;</code>s. It will look fine and mean
        <strong>nothing</strong>. Semantic tags tell the browser, search engines and screen readers
        <em>what each region is for</em>.</p>

        <h4>Div soup vs semantic layout</h4>
<pre>&lt;div class="header"&gt;      →   &lt;header&gt;
&lt;div class="nav"&gt;         →   &lt;nav&gt;
&lt;div class="main"&gt;        →   &lt;main&gt;
&lt;div class="sidebar"&gt;     →   &lt;aside&gt;
&lt;div class="footer"&gt;      →   &lt;footer&gt;</pre>

        <h4>The layout landmarks</h4>
        <table>
            <thead><tr><th>Tag</th><th>Meaning</th></tr></thead>
            <tbody>
                <tr><td><code>&lt;header&gt;</code></td><td>Introductory content — logo, page title</td></tr>
                <tr><td><code>&lt;nav&gt;</code></td><td>A block of navigation links</td></tr>
                <tr><td><code>&lt;main&gt;</code></td><td>The one unique block of content (only one per page)</td></tr>
                <tr><td><code>&lt;article&gt;</code></td><td>A self-contained piece — a blog post, a card</td></tr>
                <tr><td><code>&lt;section&gt;</code></td><td>A themed group, usually with its own heading</td></tr>
                <tr><td><code>&lt;aside&gt;</code></td><td>Tangential content — a sidebar, a tip box</td></tr>
                <tr><td><code>&lt;footer&gt;</code></td><td>Closing content — copyright, contact</td></tr>
            </tbody>
        </table>

        <h4>Why it matters</h4>
        <ul>
            <li>Screen-reader users jump between <strong>landmarks</strong> instead of listening to the whole page.</li>
            <li>Search engines understand which part is the article and which part is an advert.</li>
            <li>You stop inventing class names like <code>div-14</code>.</li>
        </ul>

        <h4>The skip link</h4>
<pre>&lt;a href="#main" class="skip-link"&gt;Skip to content&lt;/a&gt;
...
&lt;main id="main"&gt; ... &lt;/main&gt;</pre>
        <p>The first thing a keyboard user tabs to should let them jump past the navigation.</p>

        <h4>A few more</h4>
        <ul>
            <li><code>&lt;time datetime="2025-01-31"&gt;</code> — a machine-readable date.</li>
            <li><code>&lt;address&gt;</code> — contact details for the nearest article or body.</li>
            <li><code>&lt;details&gt;</code> / <code>&lt;summary&gt;</code> — a native collapsible box.</li>
            <li><code>&lt;figure&gt;</code> — any self-contained media, not just images.</li>
        </ul>
        <p>Rule of thumb: reach for a <code>&lt;div&gt;</code> only when no semantic tag fits.</p>
    `,
    visual: {
        type: 'html',
        html: `
            <div style="font-family:system-ui,sans-serif;padding:16px;font-size:.8rem;color:#1f2933;">
                <div style="border:2px dashed #7b8794;border-radius:6px;padding:8px;margin-bottom:6px;background:#f0f4f8;">
                    <strong>&lt;header&gt;</strong> — logo, page title
                </div>
                <div style="border:2px dashed #7b8794;border-radius:6px;padding:8px;margin-bottom:6px;background:#f0f4f8;">
                    <strong>&lt;nav&gt;</strong> — links
                </div>
                <div style="display:flex;gap:6px;">
                    <div style="flex:2;border:2px dashed #2563eb;border-radius:6px;padding:8px;background:#eff6ff;">
                        <strong>&lt;main&gt;</strong>
                        <div style="border:1px dashed #93c5fd;border-radius:4px;padding:6px;margin-top:6px;background:#fff;">
                            <strong>&lt;article&gt;</strong> — the actual content
                        </div>
                    </div>
                    <div style="flex:1;border:2px dashed #7b8794;border-radius:6px;padding:8px;background:#f0f4f8;">
                        <strong>&lt;aside&gt;</strong>
                    </div>
                </div>
                <div style="border:2px dashed #7b8794;border-radius:6px;padding:8px;margin-top:6px;background:#f0f4f8;">
                    <strong>&lt;footer&gt;</strong> — copyright, contact
                </div>
            </div>
        `,
    },
    challenge: {
        title: 'Boss Challenge: Rebuild the Sanctum',
        description:
    'The starter code is div soup. Replace the divs with semantic tags so the page contains a &lt;header&gt;, &lt;nav&gt;, &lt;main id="main"&gt;, &lt;article&gt;, &lt;aside&gt; and &lt;footer&gt;. Add a skip link pointing at #main, and give the page at least two &lt;h2&gt; headings inside the content.',
        starterCode:
`<body>

  <!-- Add a skip link to #main here -->

  <div class="header">
    <h1>Nova Games</h1>
  </div>

  <div class="nav">
    <a href="/">Home</a> | <a href="/games">Games</a>
  </div>

  <div class="main">
    <h2>Latest release</h2>
    <div class="post">
      <p>Bolt vs the Void is out now.</p>
    </div>

    <h2>About us</h2>
    <p>We make small games with big hearts.</p>
  </div>

  <div class="sidebar">
    <p>Tip: press M to mute.</p>
  </div>

  <div class="footer">
    <p>&copy; 2025 Nova Games</p>
  </div>

</body>`,
        hint:
`Swap each wrapper for the matching landmark:

<header> ... </header>
<nav> ... </nav>
<main id="main"> ... </main>
<article> ... </article>
<aside> ... </aside>
<footer> ... </footer>

And add at the very top of the body:
<a href="#main">Skip to content</a>`,
        xp: 60,
        slug: 'semantic-layout',
        test: (raw) => {
            const code = stripComments(raw);
            const landmarks = ['header', 'nav', 'main', 'article', 'aside', 'footer'];
            const allPresent = landmarks.every((tag) =>
                new RegExp('<' + tag + '[\\s>]', 'i').test(code));
            const skipLink = has(code, /<a[^>]*href\s*=\s*["']#main["']/i)
                          && has(code, /<main[^>]*id\s*=\s*["']main["']/i);
            const headings = count(code, /<h2[\s>]/gi) >= 2;
            return allPresent && skipLink && headings;
        },
    },
    nextLesson: 'css',
},

}; // end HTML_LESSONS