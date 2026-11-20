# lessons.py

LESSON_CONTENT = [
    {
        "slug": "html",
        "title": "HTML Basics",
        "subtitle": "The Structure of the Web",
        "icon": "HTML",
        "xp_reward": 100,
        "description": "Learn the foundation of every web page using HTML tags.",
        "duration": "10 min",
        "level": "Beginner",
        "module": "Web Fundamentals",
        "order": 1,
        "sections": [
            {
                "type": "text",
                "content": "HTML (HyperText Markup Language) is the foundation of every web page. It uses tags to structure content."
            },
            {
                "type": "code",
                "language": "html",
                "content": "<h1>Hello World!</h1>\n<p>This is a paragraph.</p>"
            },
            {
                "type": "tip",
                "content": "Always close your tags! Use </h1> to close an <h1>."
            }
        ]
    },
    {
        "slug": "css",
        "title": "CSS Styling",
        "subtitle": "Make it Look Good",
        "icon": "CSS",
        "xp_reward": 150,
        "description": "CSS controls the look and feel of your HTML. Change colors, fonts, and layouts.",
        "duration": "15 min",
        "level": "Beginner",
        "module": "Web Fundamentals",
        "order": 2,
        "sections": [
            {
                "type": "text",
                "content": "CSS (Cascading Style Sheets) is used to style HTML elements."
            },
            {
                "type": "code",
                "language": "css",
                "content": "h1 {\n  color: blue;\n  text-align: center;\n}"
            }
        ]
    },
    {
        "slug": "design",
        "title": "Design on the Web",
        "subtitle": "User Experience",
        "icon": "DSN",
        "xp_reward": 100,
        "description": "Learn how to design web pages that look great and are easy to use.",
        "duration": "20 min",
        "level": "Intermediate",
        "module": "Web Fundamentals",
        "order": 3,
        "sections": [
            {
                "type": "text",
                "content": "Good design is about making things intuitive. We will look at spacing, colors, and typography."
            }
        ]
    },
    {
        "slug": "journey",
        "title": "User Journeys",
        "subtitle": "How Users Navigate",
        "icon": "JRN",
        "xp_reward": 100,
        "description": "Map out how users move through your website from start to finish.",
        "duration": "15 min",
        "level": "Intermediate",
        "module": "Web Fundamentals",
        "order": 4,
        "sections": [
            {
                "type": "text",
                "content": "A user journey is the path a user takes when interacting with your site."
            }
        ]
    },
    {
        "slug": "js",
        "title": "JavaScript Logic",
        "subtitle": "Bring Your Page to Life",
        "icon": "js",
        "xp_reward": 200,
        "description": "JavaScript adds interactivity to web pages. Functions let you write reusable code.",
        "duration": "25 min",
        "level": "Intermediate",
        "module": "Web Fundamentals",
        "order": 5,
        "sections": [
            {
                "type": "text",
                "content": "JavaScript is the programming language of the web. It allows you to make your pages interactive."
            },
            {
                "type": "code",
                "language": "javascript",
                "content": "function greet(name) {\n  return 'Hello ' + name + '!';\n}\n\nconsole.log(greet('Student'));"
            },
            {
                "type": "tip",
                "content": "You can link a JS file to your HTML using the <script> tag."
            }
        ]
    },
    {
        "slug": "react",
        "title": "React Components",
        "subtitle": "Modern Web Apps",
        "icon": "RCT",
        "xp_reward": 300,
        "description": "Build user interfaces with reusable components using React.",
        "duration": "30 min",
        "level": "Advanced",
        "module": "Web Fundamentals",
        "order": 6,
        "sections": [
            {
                "type": "text",
                "content": "React is a library for building user interfaces based on components."
            },
            {
                "type": "code",
                "language": "jsx",
                "content": "function Welcome(props) {\n  return <h1>Hello, {props.name}!</h1>;\n}"
            }
        ]
    }
]

# Helper: lookup by slug
def get_lesson_by_slug(slug: str):
    return next((l for l in LESSON_CONTENT if l["slug"] == slug), None)