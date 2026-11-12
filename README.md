AI-Powered HTML Tutor for Young Learners
Backend Development | FastAPI · Python · SQLite · AI/ML · Gamification
> **Project:** The Impact of Gamification in an AI-Powered HTML Tutor for Young Learners  
> **Repository branch:** [`back-end`](https://github.com/Raisibe1/The-Impact-of-Gamification-in-an-AI-Powered-HTML-Tutor-for-Young-Learners/tree/back-end)  
> **Backend developer:** Sizwe Makgalelele  
> **Project focus:** Interactive HTML education and adaptive learning for young learners, particularly Grades 7–9.
1. Overview
This project explores how artificial intelligence, machine learning and gamification can support young learners as they develop foundational HTML and web-development skills.
The backend is designed to connect a learner-facing application to authentication, persistent student records, structured lessons, assessments, progress tracking and AI-assisted feedback. The goal is to support a learning journey that begins with an initial benchmark assessment, continues through guided HTML topics and evaluates performance over time.
The backend uses Python and FastAPI for HTTP services and SQLite for relational data storage. Work on the AI layer includes integration with Google Gemini for tutoring interactions and a locally served scikit-learn/joblib model for predicting learner performance.
> **Verification note:** This README documents the architecture and development work discussed for this project. The live branch could not be inspected when this version was written. File paths and endpoint examples below must be reconciled with the current branch before being treated as an authoritative inventory. Features described as *planned* or *integration work* are not claims of production readiness.
2. Backend Responsibilities
As the backend developer, my work covers:
Designing and implementing REST API endpoints with FastAPI.
Creating and maintaining relational database tables and SQL schemas.
Implementing student registration, login and server-managed cookie sessions.
Building backend functionality for lessons, assessments, progress and achievements.
Integrating the application with Gemini-powered tutoring functionality.
Preparing an ML prediction endpoint for adaptive learning.
Validating requests, handling errors and facilitating frontend/backend integration.
Preparing reproducible configuration, documentation, tests and deployment plans.
3. Technology Stack
Layer	Technology	Purpose
API framework	Python, FastAPI	API routing, validation and orchestration
ASGI server	Uvicorn	Running the application in development
Database	SQLite	Learner profiles, progress and assessment records
Data access	Python `sqlite3` / project database helpers	Queries, transactions and persistence
Authentication	Password hashing and HTTP cookies	Managing authenticated student sessions
AI tutor	Google Gemini API	Explanations and contextual learning support
ML inference	scikit-learn, joblib	Loading and serving a trained prediction model
Validation	Pydantic	Parsing and validating incoming data
Configuration	Environment variables / `.env`	Runtime secrets and configuration
API exploration	OpenAPI / Swagger UI	Interactive API documentation at `/docs`
Dependencies and package versions should be taken from the committed `requirements.txt`.
4. System Architecture
```text
                       LEARNER / FRONTEND
                  (HTML, CSS, JavaScript / UI)
                                |
                       HTTPS / JSON requests
                                |
                                v
                     FASTAPI BACKEND SERVICE
                    (API entry point / routers)
                                |
          +---------------------+---------------------+
          |                     |                     |
          v                     v                     v
   Authentication        Learning Services       AI / ML Services
   - registration        - lessons              - Gemini tutoring
   - login/logout        - benchmark            - prediction model
   - cookie session      - quizzes              - adaptive support
                         - progress
                         - achievements
          |                     |                     |
          +---------------------+---------------------+
                                |
                                v
                       SQLite DATABASE
                    (persistent learner data)
```
Typical request flow:
The frontend sends a request to an API route.
FastAPI validates the request and checks authentication where required.
A service performs the requested learning, database or AI operation.
Relevant state is read from or written to SQLite.
The backend returns a structured response and appropriate HTTP status code.
5. Repository Structure
The following is a target modular layout discussed during backend refactoring, not a verified listing of files currently in the branch:
```text
BACKEND/
├── API.py                       # FastAPI entry point (if retained)
├── .env.example                 # Safe environment-variable template
├── requirements.txt            # Python dependencies
├── core/
│   ├── config.py                # Application configuration
│   └── security.py              # Password and cookie utilities
├── database/
│   ├── connection.py            # SQLite connection helpers
│   ├── seed.py                  # Initial learning content
│   └── migrations/              # Schema changes
├── routes/                      # Auth, learning, assessment and AI routes
├── services/                    # Domain/business logic
├── models/                      # Request and response schemas
├── ml_inference.py              # Prediction model integration (if retained)
├── learning_schema.sql          # Database schema (if retained)
├── quiz_bank.json               # Assessment question bank (if retained)
└── tests/                       # Automated test suite
```
Some project versions used a flatter architecture with `API.py`, `database.py`, `lessons.py`, `connection.py` and `ml_inference.py`. Always consult the actual branch for the current module locations before modifying imports.
6. Core Backend Capabilities
6.1 Student Registration and Authentication
The application is designed to support:
Student account creation with validated details.
Password verification against stored password hashes.
Login sessions identified by a server-managed cookie (for example, `session_id`).
Protected endpoints that check whether the current learner is authenticated.
Logout/session invalidation.
The project moved away from exposing JWTs to frontend JavaScript in favour of HTTP-only cookie-based sessions. Session cookies should be configured with `HttpOnly`, `Secure` in HTTPS environments and an appropriate `SameSite` policy. The backend must also protect state-changing requests against CSRF when cookies are used.
6.2 Benchmark Assessment
A 50-mark, 30-minute HTML benchmark is part of the intended onboarding experience. It evaluates learners' prior knowledge before they begin the guided curriculum.
Assessment topics include document structure, basic tags, headings, paragraphs, hyperlinks, images, lists, tables and introductory forms/semantic HTML where appropriate.
The desired backend workflow is to deliver assessment items, enforce scoring rules, store attempts and use the results to inform the starting learning path. Verify that the current branch contains each stage of this workflow before marking it complete.
6.3 Lessons and Progress
The planned learning sequence includes:
Introduction to HTML and Web Basics.
HTML Tags and Document Structure.
Headings and Paragraphs.
Hyperlinks.
Images and Multimedia.
Lists and Tables.
Forms and User Input.
Semantic HTML and Accessibility.
Progress data can represent lesson completion, scores, attempts, time spent and prerequisite status. Database writes should use parameterized queries and transactions.
6.4 Gamification
Gamification is intended to reinforce learning through XP, badges, challenges, completion milestones and streaks. The wider product also explores educational games including Code Crossword, Snake & Ladder (Code Edition), Match Masters and Pixel Detective.
Award calculations and achievement verification should be enforced on the server, rather than trusting a score or XP value submitted by the browser. Confirm the current branch's implemented endpoints and database tables before describing particular rewards as operational.
6.5 AI-Powered Tutoring
The Gemini integration is intended to give young learners contextual explanations, hints and guidance on HTML concepts.
The backend should:
Receive and validate the learner's request.
Keep API credentials exclusively on the server.
Send an appropriately constrained prompt to Gemini.
Handle provider failures, timeouts and invalid responses gracefully.
Return a learner-friendly response without exposing private configuration.
Integration note: Previous development encountered an HTTP `401 Unauthorized` response from the Gemini service. A route being present does not mean that the provider integration is currently healthy. Verify credentials, model/API compatibility, quotas and error handling before deployment.
6.6 Machine Learning Inference
A prediction service has been developed around a serialized model artifact (for example, `synthetic_topic_mastery_predictor.joblib`). The inference layer is intended to predict the likelihood that a learner will answer the next item correctly, supporting future personalization.
Previously discussed endpoint:
```http
POST /api/predict-next-correct
Content-Type: application/json
```
The request includes a `features` object whose names and values must match the trained model's expected feature schema. The validation design checks missing or unexpected features, validates topic identifiers and rejects malformed numeric values.
Important: Do not invent feature names or use this endpoint without checking the actual model pipeline and Pydantic request schema. The model must be loaded reliably, its feature order must match training, and outputs must be checked for NaN/infinite values. A successful local prediction is not proof of model validity on real learners.
7. API Reference
FastAPI can expose generated documentation at:
`http://127.0.0.1:8000/docs` (Swagger UI)
`http://127.0.0.1:8000/redoc` (ReDoc)
`http://127.0.0.1:8000/openapi.json` (machine-readable OpenAPI specification)
Endpoint inventory requiring source verification:
Method	Route	Intended responsibility	Verification
`POST`	`/register`	Create a student account	Previously discussed; confirm branch
`POST`	`/login`	Verify credentials and establish session	Previously discussed; confirm branch
`POST`	`/api/predict-next-correct`	Run validated model inference	Previously discussed; confirm branch
`POST`	`/chat`	Send a tutoring request to Gemini	Observed in earlier development logs; confirm branch
`GET`	`/program`	Return/render the learner program page	Used in an earlier application version
`GET`	`/test`	Return/render an assessment page	Used in an earlier application version
The table is not a complete or confirmed list of current routes. Route prefixes, request bodies, response schemas and authentication requirements should be generated from the running application's OpenAPI specification. Additional learning, progress, benchmark, badge and logout endpoints may be implemented under modular routers with different paths.
Inspect the actual routes
Once the backend runs, open `/docs`, or use:
```bash
curl http://127.0.0.1:8000/openapi.json
```
For a permanent verified route inventory, export this OpenAPI document as part of your release process.
8. Database Design
The project uses SQLite (`tutor.db` in earlier implementations) for local persistent data.
Core entities discussed during development:
Entity/table	Function
`students`	Learner identity, profile and password hash
`webdev_modules`	Lesson/module metadata
`student_progress`	Completion, attempts, scores and learning progress
`code_submissions`	Submitted code and evaluation outcomes
`ai_interactions`	AI tutoring questions and responses (earlier schema)
Sessions / assessments / rewards	Additional data structures where implemented
Example relationships: a student can have multiple progress records and code submissions; modules can be associated with many students through progress records.
Design requirements:
Enable `PRAGMA foreign_keys = ON` for each SQLite connection.
Use unique constraints where appropriate, including learner email and relevant progress keys.
Hash passwords; never store plaintext passwords.
Use parameterized SQL rather than string interpolation.
Commit/rollback multi-step writes transactionally.
Maintain a reproducible schema or migration history.
Never commit production learner data or a live database with sensitive information.
9. Getting Started (Local Development)
Prerequisites
Python 3.11+ (or the version pinned by the project)
Git
A Python virtual environment
A correctly configured SQLite database/schema
Gemini credentials if testing live tutoring functionality
The trained model artifact if testing prediction functionality
Clone and select the branch
```bash
git clone https://github.com/Raisibe1/The-Impact-of-Gamification-in-an-AI-Powered-HTML-Tutor-for-Young-Learners.git
cd The-Impact-of-Gamification-in-an-AI-Powered-HTML-Tutor-for-Young-Learners
git switch back-end
```
Create and activate a virtual environment
Windows PowerShell:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```
macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Install dependencies
From the directory containing `requirements.txt`:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Configure environment variables
Create a `.env` file locally if the application uses `python-dotenv` or equivalent configuration. Example variable names used during development include:
```dotenv
GEMINI_API_KEY=replace_with_your_server_side_key
DATABASE_PATH=./tutor.db
```
> These are illustrative; the actual names must match `core/config.py` or the current application source. Never commit a real `.env` file.
Initialize the database
Use the committed migration or schema initialization script. Do not run a placeholder command against an existing database because migration strategy and seed commands vary between project versions. If the branch ships `learning_schema.sql` and it is intended for first-time initialization, an example is:
```bash
sqlite3 tutor.db < learning_schema.sql
```
This command requires the SQLite CLI and a compatible schema; it should only be run on a new database after verifying the SQL file.
Start FastAPI
If `API.py` is the entry point and defines `app = FastAPI()`:
```bash
uvicorn API:app --reload --host 127.0.0.1 --port 8000
```
If it is a package module, start it from the repository/package parent, for example:
```bash
uvicorn BACKEND.API:app --reload --host 127.0.0.1 --port 8000
```
Use whichever import path matches the committed project structure. `--reload` is for development only.
10. Frontend Integration
The learner-facing application communicates with FastAPI over JSON/HTTP. Previous frontend integration used cookie credentials:
```javascript
const response = await fetch("http://127.0.0.1:8000/api/example", {
  method: "GET",
  credentials: "include"
});

if (!response.ok) {
  throw new Error(`Request failed: ${response.status}`);
}

const data = await response.json();
```
The `/api/example` URL is a placeholder, not a real route.
If the frontend and backend run on different origins, configure CORS to allow the specific trusted frontend origin, enable credentials and ensure cookies have compatible security attributes. Do not combine credentialed requests with a wildcard allowed origin.
11. Testing Strategy
Recommended tests before a production release:
Test type	Key scenarios
Unit tests	Password helpers, scoring, progress rules, XP calculations
Database tests	CRUD, constraints, transactions and migration reproducibility
API integration tests	Registration, login, protected access, logout and error paths
Benchmark tests	Timing, answer evaluation, scoring and persisted attempts
ML tests	Missing/extra features, invalid topics, NaN/inf, prediction shape
AI integration tests	Provider success, unauthorized responses, timeouts and safe fallback
Security tests	Session fixation, cookie flags, CSRF, CORS and rate limits
End-to-end tests	Learner onboarding → benchmark → lesson → progress update
Use pytest and FastAPI's `TestClient` or an appropriate asynchronous client depending on the project. A release should report real test results, not assumed passing status.
12. Security and Learner Privacy
The platform serves minors, so privacy and safety requirements are central:
Collect only learner information required by the product.
Keep credentials out of source control and frontend bundles.
Protect private routes and verify access to each learner's records.
Enforce secure cookie settings and CSRF protections.
Apply input validation, output encoding and request-size limits.
Rate-limit login and AI chat endpoints.
Minimize sensitive data sent to external AI services.
Define retention, deletion and guardian/school consent workflows appropriate to applicable legislation (including South Africa's POPIA).
Avoid putting secrets, authentication cookies or children's personal information into logs.
Back up database data securely and test restoration.
13. Production and Deployment Readiness
Before deployment:
Confirm the actual entry point, imports, dependencies and environment variables.
Replace development configuration with production settings and HTTPS.
Verify Gemini credentials, provider compatibility and graceful failures.
Version the prediction model and confirm that training/inference schemas match.
Establish database migration, backup and restore procedures.
Add structured application logging, error monitoring and health checks.
Test authentication, CSRF, CORS, rate limiting and learner-data authorization.
Run automated integration tests and verify the full learner journey.
Document hosting requirements for the selected provider (including persistent storage and Python ASGI support).
Review the scalability limitations of SQLite before multi-instance deployment; evaluate PostgreSQL if concurrency increases.
A shared hosting plan must explicitly support persistent Python ASGI processes (or a suitable deployment mechanism); a basic static/PHP hosting package may not run FastAPI directly.
14. Current Development Status
The following statuses reflect work discussed during development, not a fresh audit of the GitHub branch:
Area	Reported/project status	Next verification
FastAPI foundation	Developed	Confirm successful startup and route list
SQLite schema/access	Developed	Confirm schema, migrations and integrity
Cookie authentication	Developed and debugged	Test full registration/login/logout cycle
HTML learning content	Developed	Confirm data loading and route integration
Benchmark	Designed; reintroduction requested	Confirm persistence and gating before lessons
Progress and gamification	Designed/under development	Verify scoring, rewards and database writes
Gemini tutor	Integration attempted; 401 error observed	Verify working provider authentication
ML prediction	Endpoint and validation developed	Verify model loading, schema and end-to-end results
Production deployment	Planned	Complete readiness checklist
15. Future Improvements
Consolidate business logic into testable services and versioned API routers.
Add continuous integration (linting, tests, dependency checks).
Improve automatic API schema publication and examples.
Add observability for response latency, error rates and model failures.
Evaluate model quality using representative learner data and appropriate consent.
Strengthen benchmark-based personalization and mastery tracking.
Improve accessibility, safety and age-appropriate feedback.
Establish a repeatable deployment and rollback process.
16. Contribution Workflow
```bash
git switch back-end
git pull origin back-end
# Make a focused change and run relevant tests
git add .
git commit -m "docs: document backend architecture and setup"
git push origin back-end
```
Before committing, verify that `.env`, `*.db`, local virtual environments, API tokens, learner data and unapproved model artifacts are excluded from version control.
17. Project Purpose
This work supports research into the impact of gamification in an AI-powered HTML tutor for young learners, combining software engineering with the educational aim of making foundational programming skills more accessible, engaging and measurable.
The backend is the system's foundation: it connects a secure learner identity to structured learning, persisted performance, AI-supported explanations and future adaptive recommendations.
---
Maintained by: Sizwe Makgalelele · Backend Developer  
Branch: `back-end`  
Documentation note: Confirm routes, filenames and completion statuses against the source tree and `/openapi.json` before publication as a verified technical specification.
