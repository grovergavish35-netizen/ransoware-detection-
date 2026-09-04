import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [traps, setTraps] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    // Fetch trap files
    fetch("http://127.0.0.1:5000/api/traps")
      .then((response) => response.json())
      .then((data) => {
        setTraps(data);
      })
      .catch((error) => {
        console.error("Error fetching traps:", error);
      });

    // Fetch security alerts
    fetch("http://127.0.0.1:5000/api/alerts")
      .then((response) => response.json())
      .then((data) => {
        setAlerts(data);
      })
      .catch((error) => {
        console.error("Error fetching alerts:", error);
      });
  }, []);

  return (
    <div className="dashboard">

      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">
          <span className="shield">🛡</span>
          <h2>RansomTrap</h2>
        </div>

        <nav>
          <a className="active">Dashboard</a>
          <a>Alerts</a>
          <a>Trap Files</a>
          <a>Process Monitor</a>
          <a>Settings</a>
        </nav>

        <div className="system-status">
          <span className="status-dot"></span>
          System Protected
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">

        <header className="topbar">
          <div>
            <h1>Security Dashboard</h1>
            <p>Real-time ransomware detection and response</p>
          </div>

          <div className="agent-status">
            <span className="green-dot"></span>
            Agent Active
          </div>
        </header>

        {/* Stats */}
        <section className="stats-grid">

          <div className="card">
            <p>System Status</p>
            <h2 className="safe">PROTECTED</h2>
          </div>

          <div className="card">
            <p>Active Trap Files</p>
            <h2>{traps.length}</h2>
          </div>

          <div className="card">
            <p>Threats Detected</p>
            <h2>{alerts.length}</h2>
          </div>

          <div className="card">
            <p>Processes Monitored</p>
            <h2>--</h2>
          </div>

        </section>

        {/* Bottom Sections */}
        <section className="content-grid">

          {/* Recent Alerts */}
          <div className="panel">
            <h3>Recent Security Alerts</h3>

            {alerts.length === 0 ? (
              <div className="empty-state">
                <div className="check">✓</div>
                <h3>No Active Threats</h3>
                <p>Your system is currently protected.</p>
              </div>
            ) : (
              alerts.map((alert) => (
                <div className="alert-item" key={alert.id}>
                  <div>
                    <strong>{alert.severity}</strong>
                    <p>{alert.detector}</p>
                    <small>{alert.timestamp}</small>
                  </div>

                  <span className="alert-status">
                    {alert.status}
                  </span>
                </div>
              ))
            )}
          </div>

          {/* Detection Engine */}
          <div className="panel">
            <h3>Detection Engine</h3>

            <div className="engine-item">
              <span>Trap File Monitor</span>
              <strong>ACTIVE</strong>
            </div>

            <div className="engine-item">
              <span>Entropy Analysis</span>
              <strong>READY</strong>
            </div>

            <div className="engine-item">
              <span>Process Monitor</span>
              <strong>ACTIVE</strong>
            </div>
          </div>

        </section>

      </main>
    </div>
  );
}

export default App;