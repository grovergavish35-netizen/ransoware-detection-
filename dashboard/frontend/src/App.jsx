import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [traps, setTraps] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [processCount, setProcessCount] = useState(0);
  const [suspiciousProcesses, setSuspiciousProcesses] = useState([]);
  const [entropyData, setEntropyData] = useState(null);
  const [riskData, setRiskData] = useState(null);
  const [lastUpdated, setLastUpdated] = useState("");
  const [simulating, setSimulating] = useState(false);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Trap Files
        const trapsResponse = await fetch(
          "http://127.0.0.1:5000/api/traps"
        );
        const trapsData = await trapsResponse.json();
        setTraps(trapsData);

        // Alerts
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
        setProcessCount(processesData.count);

        // Suspicious Processes
        const suspiciousResponse = await fetch(
          "http://127.0.0.1:5000/api/suspicious-processes"
        );
        const suspiciousData = await suspiciousResponse.json();
        setSuspiciousProcesses(
          suspiciousData.processes || []
        );

        // Entropy Analysis
        const entropyResponse = await fetch(
          "http://127.0.0.1:5000/api/entropy-status"
        );
        const entropyResult = await entropyResponse.json();
        setEntropyData(entropyResult);

        // Risk Score Engine
        const riskResponse = await fetch(
          "http://127.0.0.1:5000/api/risk-score"
        );
        const riskResult = await riskResponse.json();
        setRiskData(riskResult);

        setLastUpdated(
          new Date().toLocaleTimeString()
        );

      } catch (error) {
        console.error(
          "Error fetching dashboard data:",
          error
        );
      }
    };

    fetchDashboardData();

    const interval = setInterval(
      fetchDashboardData,
      3000
    );

    return () => clearInterval(interval);
  }, []);


  // ==========================================
  // SIMULATE ATTACK
  // ==========================================

  const handleSimulateAttack = async () => {
    try {
      setSimulating(true);

      const response = await fetch(
        "http://127.0.0.1:5000/api/simulate-attack",
        {
          method: "POST"
        }
      );

      const data = await response.json();

      if (data.success) {
        alert(
          "🚨 Simulated ransomware activity detected and contained!"
        );
      } else {
        alert("Simulation failed!");
      }

    } catch (error) {
      console.error(
        "Simulation Error:",
        error
      );

      alert("Could not connect to backend.");

    } finally {
      setSimulating(false);
    }
  };


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

          <a href="#traps">
            Trap Files
          </a>

          <a href="#process">
            Process Monitor
          </a>

          <a href="#entropy">
            Entropy Analysis
          </a>

          <a href="#risk">
            Risk Assessment
          </a>
        </nav>

        <div className="system-status">
          <span className="status-dot"></span>
          System Protected
        </div>

      </aside>


      {/* ================= MAIN CONTENT ================= */}

      <main className="main-content">

        {/* TOPBAR */}

        <header
          className="topbar"
          id="dashboard"
        >

          <div>
            <h1>Security Dashboard</h1>

            <p>
              Real-time ransomware detection and response
            </p>
          </div>


          <div className="topbar-actions">

            <button
              className="simulate-btn"
              onClick={handleSimulateAttack}
              disabled={simulating}
            >
              {simulating
                ? "SIMULATING..."
                : "🚨 SIMULATE ATTACK"}
            </button>


            <div className="agent-status">
              <span className="green-dot"></span>
              Agent Active
            </div>

          </div>

        </header>


        {/* ================= STATS ================= */}

        <section className="stats-grid">

          <div className="card">
            <p>System Status</p>
            <h2 className="safe">
              PROTECTED
            </h2>
          </div>


          <div className="card">
            <p>Active Trap Files</p>
            <h2>
              {traps.length}
            </h2>
          </div>


          <div className="card">
            <p>Threats Detected</p>
            <h2>
              {alerts.length}
            </h2>
          </div>


          <div className="card">
            <p>Processes Monitored</p>
            <h2>
              {processCount}
            </h2>
          </div>

        </section>


        {/* ================= ALERTS + ENGINE ================= */}

        <section className="content-grid">

          <div
            className="panel"
            id="alerts"
          >

            <h3>
              Recent Security Alerts
            </h3>


            {alerts.length === 0 ? (

              <div className="empty-state">

                <div className="check">
                  ✓
                </div>

                <h3>
                  No Active Threats
                </h3>

                <p>
                  Your system is currently protected.
                </p>

              </div>

            ) : (

              alerts.slice(0, 5).map(
                (alert) => (

                  <div
                    className="alert-item"
                    key={alert.id}
                  >

                    <div>

                      <strong>
                        {alert.severity}
                      </strong>

                      <p>
                        {alert.detector}
                      </p>

                      <small>
                        {alert.timestamp}
                      </small>

                    </div>


                    <span className="alert-status">
                      {alert.status}
                    </span>

                  </div>

                )
              )

            )}

          </div>


          {/* DETECTION ENGINE */}

          <div className="panel">

            <h3>
              Detection Engine
            </h3>


            <div className="engine-item">
              <span>
                Trap File Monitor
              </span>

              <strong>
                ACTIVE
              </strong>
            </div>


            <div className="engine-item">
              <span>
                Entropy Analysis
              </span>

              <strong>
                ACTIVE
              </strong>
            </div>


            <div className="engine-item">
              <span>
                Process Monitor
              </span>

              <strong>
                ACTIVE
              </strong>
            </div>


            <div className="engine-item">
              <span>
                Risk Score Engine
              </span>

              <strong>
                ACTIVE
              </strong>
            </div>


            <p
              style={{
                marginTop: "20px",
                fontSize: "12px",
                color: "#64748b"
              }}
            >
              Last updated:{" "}
              {lastUpdated || "Connecting..."}
            </p>

          </div>

        </section>


        {/* ================= SUSPICIOUS PROCESS ================= */}

        <section
          className="panel suspicious-panel"
          id="process"
        >

          <div className="suspicious-header">

            <h3>
              🔍 Suspicious Process Detection
            </h3>


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

              <div className="check">
                ✓
              </div>

              <h3>
                No Suspicious Processes
              </h3>

              <p>
                All monitored processes appear safe.
              </p>

            </div>

          ) : (

            suspiciousProcesses.map(
              (process) => (

                <div
                  className="alert-item"
                  key={process.pid}
                >

                  <div>

                    <strong>
                      {process.name}
                    </strong>

                    <p>
                      PID: {process.pid}
                    </p>

                    <small>
                      {process.reason}
                    </small>

                  </div>


                  <span className="alert-status">
                    {process.severity}
                  </span>

                </div>

              )
            )

          )}

        </section>


        {/* ================= ENTROPY ENGINE ================= */}

        <section
          className="panel suspicious-panel"
          id="entropy"
        >

          <div className="suspicious-header">

            <h3>
              📊 Entropy Analysis Engine
            </h3>


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

              <div className="check">
                ⌛
              </div>

              <h3>
                Waiting for File Analysis
              </h3>

              <p>
                Entropy engine is ready and monitoring trap files.
              </p>

            </div>

          ) : (

            <div className="entropy-details">

              <div className="entropy-score">

                <span>
                  Latest Entropy Score
                </span>

                <h1>

                  {entropyData.entropy !== null
                    ? entropyData.entropy
                    : "--"}

                </h1>

                <small>
                  Threshold:{" "}
                  {entropyData.threshold || 7.5}
                </small>

              </div>


              <div className="entropy-info">

                <p>
                  <strong>Status:</strong>{" "}
                  {entropyData.status}
                </p>


                <p>
                  <strong>
                    Last Analyzed:
                  </strong>

                  <br />

                  {entropyData.analyzed_at || "--"}

                </p>


                <p>
                  <strong>
                    File:
                  </strong>

                  <br />

                  {entropyData.file || "--"}

                </p>

              </div>

            </div>

          )}

        </section>


        {/* ================= RISK SCORE ENGINE ================= */}

        <section
          className="panel risk-panel"
          id="risk"
        >

          <div className="suspicious-header">

            <h3>
              🎯 Threat Risk Assessment
            </h3>


            <span
              className={
                riskData?.severity === "CRITICAL" ||
                riskData?.severity === "HIGH"
                  ? "danger-badge"
                  : "safe-badge"
              }
            >

              {riskData?.severity || "ANALYZING"}

            </span>

          </div>


          {!riskData ? (

            <div className="empty-state">

              <div className="check">
                ⌛
              </div>

              <h3>
                Analyzing Threat Signals
              </h3>

              <p>
                Risk engine is collecting security signals.
              </p>

            </div>

          ) : (

            <div className="risk-content">


              {/* RISK SCORE */}

              <div className="risk-score-box">

                <span>
                  Current Risk Score
                </span>

                <h1>

                  {riskData.risk_score}

                  <small>
                    /100
                  </small>

                </h1>

                <p>
                  {riskData.recommended_action}
                </p>

              </div>


              {/* DETECTION SIGNALS */}

              <div className="risk-signals">

                <h4>
                  Detection Signals
                </h4>


                {riskData.signals &&
                riskData.signals.length === 0 ? (

                  <p className="no-signals">
                    No threat signals detected.
                  </p>

                ) : (

                  riskData.signals?.map(
                    (signal, index) => (

                      <div
                        className="signal-item"
                        key={index}
                      >

                        <div>

                          <strong>
                            {signal.signal}
                          </strong>

                          <p>
                            {signal.status}
                          </p>

                        </div>


                        <span>
                          +{signal.score}
                        </span>

                      </div>

                    )
                  )

                )}

              </div>

            </div>

          )}

        </section>


      </main>

    </div>
  );
}

export default App;