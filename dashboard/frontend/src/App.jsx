import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [traps, setTraps] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [processCount, setProcessCount] = useState(0);
  const [suspiciousProcesses, setSuspiciousProcesses] = useState([]);
  const [entropyData, setEntropyData] = useState(null);
  const [riskData, setRiskData] = useState(null);
  const [responseData, setResponseData] = useState(null);
  const [lastUpdated, setLastUpdated] = useState("");
  const [simulating, setSimulating] = useState(false);
  const [containing, setContaining] = useState(false);

  // ==========================================
  // FETCH DASHBOARD DATA
  // ==========================================

  const fetchDashboardData = async () => {
    try {
      const trapsResponse = await fetch(
        "http://127.0.0.1:5000/api/traps"
      );
      const trapsData = await trapsResponse.json();
      setTraps(trapsData);

      const alertsResponse = await fetch(
        "http://127.0.0.1:5000/api/alerts"
      );
      const alertsData = await alertsResponse.json();
      setAlerts(alertsData);

      const processesResponse = await fetch(
        "http://127.0.0.1:5000/api/processes"
      );
      const processesData = await processesResponse.json();
      setProcessCount(processesData.count);

      const suspiciousResponse = await fetch(
        "http://127.0.0.1:5000/api/suspicious-processes"
      );
      const suspiciousData = await suspiciousResponse.json();
      setSuspiciousProcesses(
        suspiciousData.processes || []
      );

      const entropyResponse = await fetch(
        "http://127.0.0.1:5000/api/entropy-status"
      );
      const entropyResult = await entropyResponse.json();
      setEntropyData(entropyResult);

      const riskResponse = await fetch(
        "http://127.0.0.1:5000/api/risk-score"
      );
      const riskResult = await riskResponse.json();
      setRiskData(riskResult);

      const responseResponse = await fetch(
        "http://127.0.0.1:5000/api/threat-response"
      );
      const responseResult =
        await responseResponse.json();
      setResponseData(responseResult);

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


  // ==========================================
  // AUTO REFRESH
  // ==========================================

  useEffect(() => {
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
          "Simulated ransomware activity detected and contained!"
        );

        fetchDashboardData();
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


  // ==========================================
  // MANUAL THREAT CONTAINMENT
  // ==========================================

  const handleContainThreat = async () => {
    try {
      setContaining(true);

      const response = await fetch(
        "http://127.0.0.1:5000/api/contain-threat",
        {
          method: "POST"
        }
      );

      const data = await response.json();

      if (data.success) {
        alert(
          "Threat containment action completed successfully!"
        );

        fetchDashboardData();
      } else {
        alert("Containment failed!");
      }

    } catch (error) {
      console.error(
        "Containment Error:",
        error
      );

      alert("Could not connect to backend.");

    } finally {
      setContaining(false);
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

          <a href="#process">
            Process Monitor
          </a>

          <a href="#entropy">
            Entropy Analysis
          </a>

          <a href="#risk">
            Risk Assessment
          </a>

          <a href="#response">
            Threat Response
          </a>
        </nav>

        <div className="system-status">
          <span className="status-dot"></span>
          System Protected
        </div>

      </aside>


      {/* ================= MAIN ================= */}

      <main className="main-content">

        {/* ================= TOPBAR ================= */}

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


        {/* ================= ALERTS ================= */}

        <section className="content-grid">

          <div
            className="panel"
            id="alerts"
          >

            <h3>Recent Security Alerts</h3>

            {alerts.length === 0 ? (

              <div className="empty-state">
                <div className="check">✓</div>

                <h3>No Active Threats</h3>

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


          {/* ================= DETECTION ENGINE ================= */}

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

            <div className="engine-item">
              <span>Risk Score Engine</span>
              <strong>ACTIVE</strong>
            </div>

            <div className="engine-item">
              <span>Threat Response</span>
              <strong>ACTIVE</strong>
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


        {/* ================= PROCESS MONITOR ================= */}

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

              <div className="check">✓</div>

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


        {/* ================= ENTROPY ================= */}

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

              <div className="check">⌛</div>

              <h3>
                Waiting for File Analysis
              </h3>

              <p>
                Entropy engine is monitoring trap files.
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
                  <strong>File:</strong>

                  <br />

                  {entropyData.file || "--"}
                </p>

              </div>

            </div>

          )}

        </section>


        {/* ================= RISK SCORE ================= */}

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

              <div className="check">⌛</div>

              <h3>
                Analyzing Threat Signals
              </h3>

              <p>
                Risk engine is collecting security signals.
              </p>

            </div>

          ) : (

            <div className="risk-content">

              <div className="risk-score-box">

                <span>
                  Current Risk Score
                </span>

                <h1>
                  {riskData.risk_score}

                  <small>/100</small>
                </h1>

                <p>
                  {riskData.recommended_action}
                </p>

              </div>


              <div className="risk-signals">

                <h4>Detection Signals</h4>

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


        {/* ================= THREAT RESPONSE CENTER ================= */}

        <section
          className="panel response-panel"
          id="response"
        >

          <div className="suspicious-header">

            <h3>
              🛡️ Threat Response Center
            </h3>

            <span
              className={
                responseData?.threat_detected
                  ? "danger-badge"
                  : "safe-badge"
              }
            >
              {responseData?.status || "MONITORING"}
            </span>

          </div>


          {!responseData ? (

            <div className="empty-state">

              <div className="check">⌛</div>

              <h3>
                Checking Threat Response
              </h3>

              <p>
                Response engine is analyzing system status.
              </p>

            </div>

          ) : (

            <div className="response-content">


              <div className="response-info">

                <div className="response-row">
                  <span>
                    Recommended Action
                  </span>

                  <strong>
                    {responseData.recommended_action}
                  </strong>
                </div>


                <div className="response-row">
                  <span>
                    Response Status
                  </span>

                  <strong>
                    {responseData.response_action}
                  </strong>
                </div>


                {responseData.latest_threat && (

                  <div className="response-row">

                    <span>
                      Latest Threat
                    </span>

                    <strong>
                      {
                        responseData.latest_threat
                          .detector
                      }
                    </strong>

                  </div>

                )}

              </div>


              <div className="response-action">

                <h4>
                  Manual Response
                </h4>

                <p>
                  Trigger containment action if suspicious
                  ransomware activity is detected.
                </p>

                <button
                  className="contain-btn"
                  onClick={handleContainThreat}
                  disabled={containing}
                >
                  {containing
                    ? "CONTAINING..."
                    : "🛡️ CONTAIN THREAT"}
                </button>

              </div>

            </div>

          )}

        </section>


      </main>

    </div>
  );
}

export default App;