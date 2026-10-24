import { useState, useEffect} from "react";
import "./App.css";

function App() {
  const [page, setPage] = useState("home");

  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);

  // 3. Check auth status when the app first loads
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/me", {
          credentials: "include", // CRITICAL: Sends the HttpOnly cookie
        });
        if (response.ok) {
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.log("Not logged in");
      } finally {
        setIsCheckingAuth(false);
      }
    };
    checkAuth();
  }, []);


  const navigation = [
    ["Login", "login"],
    ["Register","register"],
    ["Dashboard", "dashboard"],
    ["AI Chatbot", "chatbot"],
    ["Progress", "progress"],
    ["Analytics", "analytics"],
    ["Play Game", "external-game"], 
  ].filter(([label,target]) => {
     if (isAuthenticated) {
      return target !== "login" && target !== "register";
    } else {
      return target !== "dashboard" && target !== "progress" && target !== "analytics"  && target !== "external-game";
    }
  });

  if(isCheckingAuth){
    return <div className="app" style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh" }}>Loading CodeVerse...</div>;
  }

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
              onClick={() => {
                if (target === "external-game") {
                  window.location.href = "http://localhost:8000/";
                } else {
                  setPage(target);
                }
              }}
            >
              {label}
            </button>
          ))}

          {/*need logout button*/}
          {isAuthenticated && (
            <button onClick={() => {
                // Clear cookie on backend (we'll add this next)
                fetch("http://localhost:8000/logout", { credentials: "include" })
                  .then(() => {
                    setIsAuthenticated(false);
                    setPage("home");
                  });
              }}
            >
              Logout
            </button>
          )}
        </nav>
      </header>

      <main>
        {page === "home" && <Home setPage={setPage} />}
        {page === "login" && <Login setIsAuthenticated={setIsAuthenticated} setPage={setPage} />}
        {page === "register" && <Register setIsAuthenticated={setIsAuthenticated} setPage={setPage} />}
        {page === "dashboard" && <Dashboard />}
        {page === "chatbot" && <Chatbot />}
        {page === "progress" && <Progress />}
        {page === "analytics" && <Analytics />}
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


function Login({setIsAuthenticated, setPage}) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async () => {
    try {
      // Connect to YOUR FastAPI backend
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      if (response.ok) {
        setMessage("Login successful!");
        setIsAuthenticated(true); // Update global state
        setPage("dashboard");      // Redirect to dashboard
      } else {
        setMessage(data.detail || "Login failed");
      }
    } catch (error) {
      setMessage("Network error. Is the backend running?");
    }
  };

  return (
    <section className="center-page">
      <div className="form-card">
        {/* ... existing UI ... */}
        <label>Email address</label>
        <input 
          type="email" 
          placeholder="Enter your email" 
          value={email}
          onChange={(e) => setEmail(e.target.value)} 
        />

        <label>Password</label>
        <input 
          type="password" 
          placeholder="Enter your password" 
          value={password}
          onChange={(e) => setPassword(e.target.value)} 
        />

        <button className="primary full" onClick={handleLogin}>Login</button>
        {message && <p className="small-text">{message}</p>}
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
  // State to hold the current text in the input box
  const [input, setInput] = useState("");
  
  // State to hold the conversation history
  const [messages, setMessages] = useState([
    { sender: "ai", text: "Hello. I'm your HTML tutor. Ask me anything about your lesson." }
  ]);
  
  // State to show a loading indicator while waiting for your backend
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    // Don't send empty messages
    if (!input.trim()) return;

    const userMessage = input;
    
    // 1. Add the user's message to the chat history immediately
    setMessages((prev) => [...prev, { sender: "user", text: userMessage }]);
    setInput(""); // Clear the input box
    setIsLoading(true); // Show loading state

    try {
      // 2. Make the POST request to your FastAPI backend
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        // This is the JSON payload your FastAPI backend will receive: {"message": "user's text"}
        body: JSON.stringify({ message: userMessage }), 
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      // 3. Parse the JSON response from your backend
      const data = await response.json();
      
      // 4. Add the AI's response to the chat history
      // NOTE: Change 'data.reply' to whatever key your FastAPI endpoint returns (e.g., data.response, data.answer)
      setMessages((prev) => [
        ...prev, 
        { sender: "ai", text: data.reply || data.response || "Sorry, I didn't catch that." }
      ]);

    } catch (error) {
      console.error("Error connecting to backend:", error);
      // Add an error message to the chat if the backend is down
      setMessages((prev) => [
        ...prev, 
        { sender: "ai", text: "Error: Could not connect to the tutor server." }
      ]);
    } finally {
      setIsLoading(false); // Stop the loading state
    }
  };

  // Allow sending with the "Enter" key
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  return (
    <section className="chatbot-page page-section">
      <div className="section-heading">
        <p className="label">AI CHATBOT</p>
        <h2>Your HTML tutor.</h2>
        <p>Ask me anything about your HTML lesson.</p>
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
          {/* Map through the messages array to display the conversation */}
          <div className="chat-history" style={{ display: "flex", flexDirection: "column", gap: "10px", marginBottom: "20px" }}>
            {messages.map((msg, index) => (
              <div 
                key={index} 
                className={`chat-message ${msg.sender === "user" ? "message-user" : "message-ai"}`}
                style={{
                  alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
                  backgroundColor: msg.sender === "user" ? "#0A3323" : "#f0f0f0",
                  color: msg.sender === "user" ? "#ffffff" : "#000000",
                  padding: "10px 15px",
                  borderRadius: "10px",
                  maxWidth: "80%"
                }}
              >
                {msg.text}
              </div>
            ))}
            {isLoading && <div className="chat-message message-ai" style={{ alignSelf: "flex-start", fontStyle: "italic", color: "#888" }}>Tutor is typing...</div>}
          </div>

          <div className="chat-input" style={{ display: "flex", gap: "10px" }}>
            <input 
              type="text"
              placeholder="Ask a question about HTML..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isLoading}
              style={{ flex: 1, padding: "10px" }}
            />
            <button onClick={handleSend} disabled={isLoading}>
              {isLoading ? "Sending..." : "Send"}
            </button>
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

function Register({ setIsAuthenticated, setPage }) { // <--- CHANGE 1: Added props
  // State to hold all the form data matching your students table schema
  const [formData, setFormData] = useState({
    name: "",
    surname: "",
    school: "",
    email: "",
    password: "",
    age_group: "",
    learning_style: "",
    goal: "",
  });

  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Handle changes for all inputs
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault(); // Prevent page reload
    setIsLoading(true);
    setMessage("");

    try {
      const response = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // <--- CHANGE 2: Receive the HttpOnly cookie
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("Registration successful! You can now log in.");
        
        // Optionally clear the form here
        setFormData({
          name: "", surname: "", school: "", email: "",
          password: "", age_group: "", learning_style: "", goal: "",
        });

        // <--- CHANGE 3: Update global auth state and redirect
        setIsAuthenticated(true); 
        setPage("dashboard");      
      } else {
        // FastAPI sends error details in data.detail
        setMessage(data.detail || "Registration failed. Please check your details.");
      }
    } catch (error) {
      console.error("Registration error:", error);
      setMessage("Network error. Is the backend running?");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="center-page">
      <div className="form-card" style={{ maxWidth: "500px" }}>
        <p className="label">JOIN CODEVERSE</p>
        <h2>Create your learner profile</h2>
        <p className="description">Start your HTML learning journey today.</p>

        <form onSubmit={handleRegister} style={{ display: "flex", flexDirection: "column", gap: "15px", textAlign: "left" }}>
          
          <div style={{ display: "flex", gap: "10px" }}>
            <div style={{ flex: 1 }}>
              <label>Name</label>
              <input
                type="text"
                name="name"
                placeholder="First name"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </div>
            <div style={{ flex: 1 }}>
              <label>Surname</label>
              <input
                type="text"
                name="surname"
                placeholder="Last name"
                value={formData.surname}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <label>School</label>
          <input
            type="text"
            name="school"
            placeholder="Your school"
            value={formData.school}
            onChange={handleChange}
            required
          />

          <label>Email address</label>
          <input
            type="email"
            name="email"
            placeholder="Enter your email"
            value={formData.email}
            onChange={handleChange}
            required
          />

          <label>Password</label>
          <input
            type="password"
            name="password"
            placeholder="Min 8 characters"
            value={formData.password}
            onChange={handleChange}
            required
            minLength={8}
          />

          <label>Age Group</label>
          <select name="age_group" value={formData.age_group} onChange={handleChange}>
            <option value="">Select age group (optional)</option>
            <option value="8-12">8-12</option>
            <option value="13-15">13-15</option>
            <option value="16-18">16-18</option>
            <option value="18+">18+</option>
          </select>

          <label>Learning Style</label>
          <select name="learning_style" value={formData.learning_style} onChange={handleChange}>
            <option value="">Select learning style (optional)</option>
            <option value="visual">Visual</option>
            <option value="auditory">Auditory</option>
            <option value="kinesthetic">Kinesthetic</option>
            <option value="reading">Reading/Writing</option>
          </select>

          <label>Goal</label>
          <input
            type="text"
            name="goal"
            placeholder="What do you want to achieve?"
            value={formData.goal}
            onChange={handleChange}
            required
          />

          <button type="submit" className="primary full" disabled={isLoading} style={{ marginTop: "10px" }}>
            {isLoading ? "Registering..." : "Register"}
          </button>
        </form>

        {message && (
          <p className="small-text" style={{ color: message.includes("successful") ? "green" : "red", marginTop: "15px", fontWeight: "bold" }}>
            {message}
          </p>
        )}
      </div>
    </section>
  );
}

export default App;