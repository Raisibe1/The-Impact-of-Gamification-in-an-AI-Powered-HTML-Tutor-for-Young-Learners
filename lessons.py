# lesson_content.py
# Each lesson: metadata + ordered sections.
# Section types recognised by the frontend: "text" | "code" | "tip".
LESSON_CONTENT = [
    {
        "slug": "introduction-to-html",
        "title": "Introduction to HTML",
        "subtitle": "The Language of the Web",   
        "icon": "HTML",                          
        "xp_reward": 15,                         
        "description": "Discover what HTML is, why it exists, and how every web page is built from it.",
        "duration": "10 min",
        "level": "Beginner",
        "module": "HTML Fundamentals",
        "order": 1,
        "sections": [
            {
                "type": "text",
                "content": (
                    "HTML stands for HyperText Markup Language. It is the standard "
                    "language used to create the structure of every web page on the "
                    "internet. When you visit a website, your browser reads the HTML "
                    "and turns it into the page you see."
                ),
            },
            {
                "type": "text",
                "content": (
                    "HTML is made up of elements. An element is written using tags — "
                    "opening and closing tags wrapped in angle brackets. Together, "
                    "they tell the browser what each piece of content is."
                ),
            },
            {
                "type": "code",
                "language": "html",
                "content": (
                    "<!DOCTYPE html>\n"
                    "<html>\n"
                    "  <head>\n"
                    "    <title>My First Page</title>\n"
                    "  </head>\n"
                    "  <body>\n"
                    "    <h1>Hello, world!</h1>\n"
                    "    <p>This is my very first HTML page.</p>\n"
                    "  </body>\n"
                    "</html>"
                ),
            },
            {
                "type": "tip",
                "content": (
                    "Every HTML document starts with <!DOCTYPE html>. It tells the "
                    "browser to use modern HTML rules."
                ),
            },
            {
                "type": "text",
                "content": (
                    "The <html> element wraps everything. Inside it, <head> holds "
                    "information about the page (like the title) and <body> holds the "
                    "content the user actually sees."
                ),
            },
        ],
    },
    {
        "slug": "headings-and-paragraphs",
        "title": "Headings and Paragraphs",
        "subtitle": "Structuring Your Text",   
        "icon": "H1",                            
        "xp_reward": 15,                         
        "description": "Learn how to structure text using h1–h6 headings and p paragraphs.",
        "duration": "12 min",
        "level": "Beginner",
        "module": "HTML Fundamentals",
        "order": 2,
        "sections": [
            {
                "type": "text",
                "content": (
                    "Headings organise your content into sections. HTML gives you six "
                    "levels of headings, from <h1> (most important) down to <h6> "
                    "(least important)."
                ),
            },
            {
                "type": "code",
                "language": "html",
                "content": (
                    "<h1>Main title</h1>\n"
                    "<h2>Section title</h2>\n"
                    "<h3>Subsection</h3>\n"
                    "<p>This is a paragraph of text.</p>"
                ),
            },
            {
                "type": "text",
                "content": (
                    "Paragraphs are written with the <p> tag. Browsers automatically "
                    "add space above and below paragraphs, so you do not need to "
                    "insert blank lines manually."
                ),
            },
            {
                "type": "tip",
                "content": "Only use one <h1> per page. It should describe the main topic.",
            },
        ],
    },
    {
        "slug": "links-and-images",
        "title": "Links and Images",
        "subtitle": "Connecting and Showing",  
        "icon": "A/IMG",                         
        "xp_reward": 20,
        "description": "Connect pages together with <a> and bring them to life with <img>.",
        "duration": "15 min",
        "level": "Beginner",
        "module": "HTML Fundamentals",
        "order": 3,
        "sections": [
            {
                "type": "text",
                "content": (
                    "Links are what make the web a web. The <a> element creates a "
                    "link, and its href attribute tells the browser where to go."
                ),
            },
            {
                "type": "code",
                "language": "html",
                "content": (
                    '<a href="https://example.com">Visit Example</a>\n\n'
                    '<img src="cat.jpg" alt="A small cat" />'
                ),
            },
            {
                "type": "text",
                "content": (
                    "Images use the <img> tag. It is self-closing — no separate "
                    "closing tag. The src attribute points to the image file, and "
                    "alt describes the image for screen readers."
                ),
            },
            {
                "type": "tip",
                "content": (
                    "Always add alt text to images. It helps visually impaired users "
                    "and appears when the image fails to load."
                ),
            },
        ],
    },
    {
        "slug": "lists",
        "title": "Lists",
        "subtitle": "Grouping Related Items",  
        "icon": "UL",                            
        "xp_reward": 15,
        "description": "Ordered and unordered lists help you group related items.",
        "duration": "10 min",
        "level": "Beginner",
        "module": "HTML Fundamentals",
        "order": 4,
        "sections": [
            {
                "type": "text",
                "content": (
                    "Lists group related items together. Use <ul> for unordered "
                    "(bulleted) lists and <ol> for ordered (numbered) lists. Each "
                    "item goes inside an <li> tag."
                ),
            },
            {
                "type": "code",
                "language": "html",
                "content": (
                    "<ul>\n"
                    "  <li>HTML</li>\n"
                    "  <li>CSS</li>\n"
                    "  <li>JavaScript</li>\n"
                    "</ul>\n\n"
                    "<ol>\n"
                    "  <li>Wake up</li>\n"
                    "  <li>Write code</li>\n"
                    "  <li>Repeat</li>\n"
                    "</ol>"
                ),
            },
            {
                "type": "tip",
                "content": "Lists can be nested — just place a new <ul> or <ol> inside an <li>.",
            },
        ],
    },
    {
        "slug": "forms-and-inputs",
        "title": "Forms and Inputs",
        "subtitle": "Collecting User Input",     
        "icon": "FORM",                         
        "xp_reward": 25,
        "description": "Collect information from users with form elements.",
        "duration": "18 min",
        "level": "Intermediate",
        "module": "HTML Fundamentals",
        "order": 5,
        "sections": [
            {
                "type": "text",
                "content": (
                    "Forms let users send information back to a website — like a "
                    "login, a search box, or a contact form. Everything lives inside "
                    "a <form> element."
                ),
            },
            {
                "type": "code",
                "language": "html",
                "content": (
                    '<form>\n'
                    '  <label for="name">Your name</label>\n'
                    '  <input id="name" type="text" />\n\n'
                    '  <label for="email">Your email</label>\n'
                    '  <input id="email" type="email" />\n\n'
                    '  <button type="submit">Send</button>\n'
                    '</form>'
                ),
            },
            {
                "type": "tip",
                "content": "Every input should have a matching <label> so users know what to type.",
            },
        ],
    },
]

# Helper: lookup by slug
def get_lesson_by_slug(slug: str):
    return next((l for l in LESSON_CONTENT if l["slug"] == slug), None)