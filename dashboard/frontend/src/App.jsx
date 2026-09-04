import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [traps, setTraps] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [processCount, setProcessCount] = useState(0);
  const [suspiciousProcesses, setSuspiciousProcesses] = useState([]);
  const [entropyData, setEntropyData] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [lastUpdated, setLastUpdated] = useState("");

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Trap Files
        const trapsResponse = await fetch(
          "http://127.0.0.1:5000/api/traps"
        );
        const trapsData = await trapsResponse.json();
        setTraps(trapsData);

        // Security Alerts
        const alertsResponse = await fetch(
          "http://127.0.0.1:5000/api/alerts"
        );
        const alertsData = await alertsResponse.json();
        setAlerts(alertsData);

        // Process Count
        const processesResponse = await fetch(
          "http://127.0.0.1:5000/api/processes"
        );
        const processesData = await processesResponse.json();
        setProcessCount(processesData.count || 0);

        // Suspicious Processes
        const suspiciousResponse = await fetch(
          "http://127.0.0.1:5000/api/suspicious-processes"
        );
        const suspiciousData = await suspiciousResponse.json();
        setSuspiciousProcesses(suspiciousData.processes || []);

        // Latest Entropy Analysis
        const entropyResponse = await fetch(
          "http://127.0.0.1:5000/api/entropy-status"
        );
        const entropyResult = await entropyResponse.json();
        setEntropyData(entropyResult);

        // Threat Timeline
        const timelineResponse = await fetch(
          "http://127.0.0.1:5000/api/timeline"
        );
        const timelineData = await timelineResponse.json();
        setTimeline(Array.isArray(timelineData) ? timelineData : []);

        setLastUpdated(new Date().toLocaleTimeString());

      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      }
    };

    fetchDashboardData();

    // Auto refresh every 3 seconds
    const interval = setInterval(fetchDashboardData, 3000);

    return () => clearInterval(interval);
  }, []);


  return (
    <div className="dashboard">

      {/* ================= SIDEBAR ================= */}
      <aside className="sidebar">

        <div className="logo">
          <span className="shield">🛡️</span>
          <h2>RansomTrap</h2>
        </div>

        <nav>
          <a href="#dashboard" className="active">
            Dashboard
          </a>

          <a href="#alerts">
            Alerts
          </a>

          <a href="#process">
            Process Monitor
          </a>

          <a href="#entropy">
            Entropy Analysis
          </a>

          <a href="#timeline">
            Threat Timeline
          </a>
        </nav>

        <div className="system-status">
          <span className="status-dot"></span>
          System Protected
        </div>

      </aside>


      {/* ================= MAIN CONTENT ================= */}
      <main className="main-content">

        {/* HEADER */}
        <header className="topbar" id="dashboard">

          <div>
            <h1>Security Dashboard</h1>
            <p>
              Real-time ransomware detection and response
            </p>
          </div>

          <div className="agent-status">
            <span className="green-dot"></span>
            Agent Active
          </div>

        </header>


        {/* ================= STATS ================= */}
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
            <h2>{processCount}</h2>
          </div>

        </section>


        {/* ================= ALERTS + ENGINE ================= */}
        <section className="content-grid">

          {/* Recent Alerts */}
          <div className="panel" id="alerts">

            <h3>Recent Security Alerts</h3>

            {alerts.length === 0 ? (

              <div className="empty-state">
                <div className="check">✓</div>
                <h3>No Active Threats</h3>
                <p>Your system is currently protected.</p>
              </div>

            ) : (

              alerts.slice(0, 5).map((alert) => (

                <div
                  className="alert-item"
                  key={alert.id}
                >

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
              <strong>ACTIVE</strong>
            </div>

            <div className="engine-item">
              <span>Process Monitor</span>
              <strong>ACTIVE</strong>
            </div>

            <p
              style={{
                marginTop: "20px",
                fontSize: "12px",
                color: "#64748b"
              }}
            >
              Last updated: {lastUpdated || "Connecting..."}
            </p>

          </div>

        </section>


        {/* ================= PROCESS MONITOR ================= */}
        <section
          className="panel suspicious-panel"
          id="process"
        >

          <div className="suspicious-header">

            <h3>🔍 Suspicious Process Detection</h3>

            <span
              className={
                suspiciousProcesses.length > 0
                  ? "danger-badge"
                  : "safe-badge"
              }
            >

              {suspiciousProcesses.length > 0
                ? `${suspiciousProcesses.length} THREAT(S)`
                : "NO THREATS"}

            </span>

          </div>


          {suspiciousProcesses.length === 0 ? (

            <div className="empty-state">

              <div className="check">✓</div>

              <h3>No Suspicious Processes</h3>

              <p>
                All monitored processes appear safe.
              </p>

            </div>

          ) : (

            suspiciousProcesses.map((process) => (

              <div
                className="alert-item"
                key={process.pid}
              >

                <div>
                  <strong>{process.name}</strong>
                  <p>PID: {process.pid}</p>
                  <small>{process.reason}</small>
                </div>

                <span className="alert-status">
                  {process.severity}
                </span>

              </div>

            ))

          )}

        </section>


        {/* ================= ENTROPY ANALYSIS ================= */}
        <section
          className="panel suspicious-panel"
          id="entropy"
        >

          <div className="suspicious-header">

            <h3>📊 Entropy Analysis Engine</h3>

            <span
              className={
                entropyData?.suspicious
                  ? "danger-badge"
                  : "safe-badge"
              }
            >

              {entropyData?.status || "WAITING"}

            </span>

          </div>


          {!entropyData ||
          entropyData.status === "WAITING" ? (

            <div className="empty-state">

              <div className="check">⌛</div>

              <h3>Waiting for File Analysis</h3>

              <p>
                Entropy engine is ready and monitoring trap files.
              </p>

            </div>

          ) : (

            <div className="entropy-details">

              <div className="entropy-score">

                <span>Latest Entropy Score</span>

                <h1>
                  {entropyData.entropy !== null
                    ? entropyData.entropy
                    : "--"}
                </h1>

                <small>
                  Threshold: {entropyData.threshold || 7.5}
                </small>

              </div>


              <div className="entropy-info">

                <p>
                  <strong>Status:</strong>
                  {" "}
                  {entropyData.status}
                </p>

                <p>
                  <strong>Last Analyzed:</strong>
                  <br />
                  {entropyData.analyzed_at || "--"}
                </p>

                <p>
                  <strong>File:</strong>
                  <br />
                  {entropyData.file || "--"}
                </p>

              </div>

            </div>

          )}

        </section>


        {/* ================= THREAT TIMELINE ================= */}
        <section
          className="panel suspicious-panel"
          id="timeline"
        >

          <div className="suspicious-header">

            <h3>⚡ Recent Threat Timeline</h3>

            <span className="danger-badge">
              LIVE EVENTS
            </span>

          </div>


          {timeline.length === 0 ? (

            <div className="empty-state">

              <div className="check">✓</div>

              <h3>No Security Events</h3>

              <p>
                System activity will appear here.
              </p>

            </div>

          ) : (

            <div className="timeline-container">

              {timeline.map((event) => (

                <div
                  className="timeline-item"
                  key={event.id}
                >

                  <div className="timeline-dot"></div>


                  <div className="timeline-content">

                    <div className="timeline-header">

                      <strong>
                        {event.detector}
                      </strong>

                      <span className="timeline-time">
                        {event.timestamp}
                      </span>

                    </div>


                    <p>
                      {event.action}
                    </p>


                    <div className="timeline-footer">

                      <span className="timeline-severity">
                        {event.severity}
                      </span>

                      <span className="timeline-status">
                        {event.status}
                      </span>

                    </div>

                  </div>

                </div>

              ))}

            </div>

          )}

        </section>

      </main>

    </div>
  );
}

export default App;