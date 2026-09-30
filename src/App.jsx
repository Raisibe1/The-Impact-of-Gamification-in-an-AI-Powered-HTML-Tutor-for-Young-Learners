import { useState } from "react";
import "./App.css";

function App() {
  const [page, setPage] = useState("home");

  const navigation = [
    ["Login", "login"],
    ["Dashboard", "dashboard"],
    ["AI Chatbot", "chatbot"],
    ["Progress", "progress"],
    ["Analytics", "analytics"],
    ["Profile", "profile"],
  ];

  return (
    <div className="app">
      <header className="navbar">
        <button className="logo" onClick={() => setPage("home")}>
          <span className="logo-shape">&lt;/&gt;</span>
          <span>
            <strong>CodeVerse</strong>
            <small>HTML LEARNING</small>
          </span>
        </button>

        <nav>
          {navigation.map(([label, target]) => (
            <button
              key={target}
              className={page === target ? "nav-active" : ""}
              onClick={() => setPage(target)}
            >
              {label}
            </button>
          ))}
        </nav>
      </header>

      <main>
        {page === "home" && <Home setPage={setPage} />}
        {page === "login" && <Login />}
        {page === "dashboard" && <Dashboard />}
        {page === "chatbot" && <Chatbot />}
        {page === "progress" && <Progress />}
        {page === "analytics" && <Analytics />}
        {page === "profile" && <Profile />}
      </main>

      <footer>
        <span>CodeVerse</span>
        <span>HTML Learning Platform</span>
      </footer>
    </div>
  );
}

function Home({ setPage }) {
  return (
    <section className="home">
      <div className="home-content">
        <p className="label">WELCOME TO CODEVERSE</p>

        <h1>
          Learn HTML.
          <br />
          <span>Build your first website.</span>
        </h1>

        <p className="intro">
          A simple and interactive way to learn HTML through guided lessons,
          an AI tutor, practice activities and personalised progress.
        </p>

        <div className="buttons">
          <button className="primary" onClick={() => setPage("login")}>
            Start Learning
          </button>

          <button className="secondary" onClick={() => setPage("dashboard")}>
            Explore Platform
          </button>
        </div>

        <div className="html-tags">
          <span>&lt;html&gt;</span>
          <span>&lt;body&gt;</span>
          <span>&lt;h1&gt;</span>
          <span>&lt;p&gt;</span>
        </div>
      </div>

      <div className="illustration-area">
        <div className="illustration-card">
          <div className="window">
            <div className="window-top">
              <span></span>
              <span></span>
              <span></span>
            </div>

            <div className="code">
              <p>
                <b>&lt;html&gt;</b>
              </p>

              <p className="indent">
                <b>&lt;body&gt;</b>
              </p>

              <p className="indent-two">
                <b>&lt;h1&gt;</b>
                <em>Hello World</em>
                <b>&lt;/h1&gt;</b>
              </p>

              <p className="indent-two">
                <b>&lt;p&gt;</b>
                <em>Welcome to HTML</em>
                <b>&lt;/p&gt;</b>
              </p>

              <p className="indent">
                <b>&lt;/body&gt;</b>
              </p>

              <p>
                <b>&lt;/html&gt;</b>
              </p>
            </div>
          </div>

          <div className="paper-illustration">
            <div className="paper-line long"></div>
            <div className="paper-line"></div>
            <div className="paper-line short"></div>
          </div>

          <div className="plant-illustration">
            <div className="stem"></div>
            <div className="leaf left"></div>
            <div className="leaf right"></div>
          </div>
        </div>
      </div>
    </section>
  );
}

function Login() {
  return (
    <section className="center-page">
      <div className="form-card">
        <div className="form-illustration"></div>

        <p className="label">WELCOME BACK</p>

        <h2>Log in to CodeVerse</h2>

        <p className="description">
          Continue your HTML learning journey.
        </p>

        <label>Email address</label>
        <input type="email" placeholder="Enter your email" />

        <label>Password</label>
        <input type="password" placeholder="Enter your password" />

        <button className="primary full">Login</button>

        <p className="small-text">
          New to CodeVerse? Create your learner profile.
        </p>
      </div>
    </section>
  );
}

function Dashboard() {
  return (
    <section className="dashboard page-section">
      <div className="section-heading">
        <p className="label">DASHBOARD</p>
        <h2>Welcome to your learning space.</h2>
        <p>
          Your HTML lessons, activities and learning journey will appear here.
        </p>
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-card large-card">
          <div className="card-illustration html-illustration">
            <span>&lt;/&gt;</span>
          </div>

          <div>
            <p className="label">CURRENT COURSE</p>
            <h3>HTML Fundamentals</h3>
            <p>
              Learn the structure of webpages and start creating your own HTML
              documents.
            </p>
            <button className="primary">Continue Learning</button>
          </div>
        </div>

        <div className="dashboard-card">
          <p className="label">NEXT LESSON</p>
          <h3>HTML Elements</h3>
          <p>Learn how tags create the structure of a webpage.</p>
          <div className="fake-progress">
            <span></span>
          </div>
          <small>Lesson 1 of 5</small>
        </div>

        <div className="dashboard-card">
          <p className="label">AI TUTOR</p>
          <h3>Ask your tutor</h3>
          <p>
            Your HTML tutor will help explain concepts whenever you need
            clarification.
          </p>
          <button className="secondary">Open AI Chatbot</button>
        </div>
      </div>
    </section>
  );
}

function Chatbot() {
  return (
    <section className="chatbot-page page-section">
      <div className="section-heading">
        <p className="label">AI CHATBOT</p>
        <h2>Your HTML tutor.</h2>
        <p>
          This is the frontend interface for your future AI-powered HTML
          tutor.
        </p>
      </div>

      <div className="chat-container">
        <div className="tutor-illustration">
          <div className="tutor-head">
            <div className="eye"></div>
            <div className="eye"></div>
          </div>
          <div className="tutor-body"></div>
        </div>

        <div className="chat-content">
          <div className="chat-message">
            Hello. I'm your HTML tutor. Ask me anything about your lesson.
          </div>

          <div className="chat-input">
            <span>Ask a question about HTML...</span>
            <button>Send</button>
          </div>
        </div>
      </div>
    </section>
  );
}

function Progress() {
  return (
    <section className="page-section">
      <div className="section-heading">
        <p className="label">YOUR PROGRESS</p>
        <h2>Track your HTML journey.</h2>
        <p>Your learning progress will appear here.</p>
      </div>

      <div className="progress-card">
        <div className="progress-number">20%</div>

        <div>
          <h3>HTML Fundamentals</h3>
          <p>Lesson 1 of 5 completed.</p>

          <div className="large-progress">
            <span></span>
          </div>
        </div>
      </div>
    </section>
  );
}

function Analytics() {
  return (
    <section className="empty-page">
      <div className="empty-illustration"></div>
      <p className="label">ANALYTICS</p>
      <h2>Your learning analytics.</h2>
    </section>
  );
}

function Profile() {
  return (
    <section className="profile-page">
      <div className="profile-illustration"></div>

      <p className="label">PROFILE</p>
      <h2>Your learner profile.</h2>

      <div className="profile-form">
        <label>Name</label>
        <input placeholder="Learner name" />

        <label>Email</label>
        <input placeholder="Learner email" />

        <button className="primary">Save Profile</button>
      </div>
    </section>
  );
}

export default App;