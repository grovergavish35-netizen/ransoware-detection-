import { useEffect, useState } from "react";
import "./App.css";

import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts";

function App() {
  const [traps, setTraps] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [processCount, setProcessCount] = useState(0);
  const [suspiciousProcesses, setSuspiciousProcesses] = useState([]);
  const [entropyData, setEntropyData] = useState(null);
  const [riskData, setRiskData] = useState(null);
  const [responseData, setResponseData] = useState(null);
  const [timelineData, setTimelineData] = useState([]);
  const [backupData, setBackupData] = useState(null);

  const [lastUpdated, setLastUpdated] = useState("");
  const [simulating, setSimulating] = useState(false);
  const [containing, setContaining] = useState(false);
  const [creatingBackup, setCreatingBackup] = useState(false);

  // ==========================================
  // SECURITY ANALYTICS DATA
  // ==========================================

  const analyticsData = [
    {
      name: "LOW",
      value: alerts.filter(
        (alert) => alert.severity === "LOW"
      ).length,
    },
    {
      name: "MEDIUM",
      value: alerts.filter(
        (alert) => alert.severity === "MEDIUM"
      ).length,
    },
    {
      name: "HIGH",
      value: alerts.filter(
        (alert) => alert.severity === "HIGH"
      ).length,
    },
    {
      name: "CRITICAL",
      value: alerts.filter(
        (alert) => alert.severity === "CRITICAL"
      ).length,
    },
  ].filter((item) => item.value > 0);


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


      const timelineResponse = await fetch(
        "http://127.0.0.1:5000/api/threat-timeline"
      );
      const timelineResult =
        await timelineResponse.json();
      setTimelineData(
        timelineResult.events || []
      );


      const backupResponse = await fetch(
        "http://127.0.0.1:5000/api/backup-status"
      );
      const backupResult =
        await backupResponse.json();
      setBackupData(backupResult);


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
          method: "POST",
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
          method: "POST",
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


  // ==========================================
  // CREATE BACKUP
  // ==========================================

  const handleCreateBackup = async () => {
    try {
      setCreatingBackup(true);

      const response = await fetch(
        "http://127.0.0.1:5000/api/create-backup",
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (data.success) {
        alert(
          "Protected backup created successfully!"
        );

        fetchDashboardData();
      } else {
        alert("Backup creation failed!");
      }

    } catch (error) {
      console.error(
        "Backup Error:",
        error
      );

      alert(
        "Could not connect to backup service."
      );

    } finally {
      setCreatingBackup(false);
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

          <a href="#analytics">
            Security Analytics
          </a>

          <a href="#timeline">
            Activity Timeline
          </a>

          <a href="#backup">
            Backup & Recovery
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

            <div className="engine-item">
              <span>Security Analytics</span>
              <strong>ACTIVE</strong>
            </div>

            <div className="engine-item">
              <span>Activity Timeline</span>
              <strong>ACTIVE</strong>
            </div>

            <div className="engine-item">
              <span>Backup & Recovery</span>
              <strong>ACTIVE</strong>
            </div>

            <p
              style={{
                marginTop: "20px",
                fontSize: "12px",
                color: "#64748b",
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


        {/* ================= THREAT RESPONSE ================= */}

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
                      {responseData.latest_threat.detector}
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


        {/* ================= SECURITY ANALYTICS ================= */}

        <section
          className="panel analytics-panel"
          id="analytics"
        >

          <div className="suspicious-header">

            <div>
              <h3>📊 Security Analytics</h3>

              <p className="analytics-subtitle">
                Threat distribution based on recorded security events
              </p>
            </div>

            <span className="safe-badge">
              {alerts.length} TOTAL EVENTS
            </span>

          </div>


          <div className="analytics-content">

            <div className="chart-container">

              {analyticsData.length === 0 ? (

                <div className="empty-state">

                  <div className="check">✓</div>

                  <h3>
                    No Analytics Available
                  </h3>

                  <p>
                    Security events will appear here once detected.
                  </p>

                </div>

              ) : (

                <ResponsiveContainer
                  width="100%"
                  height={320}
                >

                  <PieChart>

                    <Pie
                      data={analyticsData}
                      cx="50%"
                      cy="50%"
                      innerRadius={70}
                      outerRadius={110}
                      paddingAngle={4}
                      dataKey="value"
                    >

                      {analyticsData.map(
                        (entry, index) => (

                          <Cell
                            key={`cell-${index}`}
                            fill={
                              entry.name === "LOW"
                                ? "#22c55e"
                                : entry.name === "MEDIUM"
                                ? "#eab308"
                                : entry.name === "HIGH"
                                ? "#f97316"
                                : "#ef4444"
                            }
                          />

                        )
                      )}

                    </Pie>

                    <Tooltip />
                    <Legend />

                  </PieChart>

                </ResponsiveContainer>

              )}

            </div>


            <div className="analytics-summary">

              <h4>Threat Summary</h4>

              {["LOW", "MEDIUM", "HIGH", "CRITICAL"].map(
                (severity) => (

                  <div
                    className={`analytics-stat ${severity.toLowerCase()}`}
                    key={severity}
                  >

                    <div>
                      <span className="analytics-dot"></span>
                      {severity}
                    </div>

                    <strong>
                      {
                        alerts.filter(
                          (alert) =>
                            alert.severity === severity
                        ).length
                      }
                    </strong>

                  </div>

                )
              )}


              <div className="analytics-total">

                <span>
                  Total Recorded Events
                </span>

                <h2>
                  {alerts.length}
                </h2>

              </div>

            </div>

          </div>

        </section>


        {/* ================= BACKUP & RECOVERY ================= */}

        <section
          className="panel backup-panel"
          id="backup"
        >

          <div className="suspicious-header">

            <div>
              <h3>
                💾 Backup & Recovery Center
              </h3>

              <p className="analytics-subtitle">
                Protected file backups for ransomware recovery
              </p>
            </div>

            <span className="safe-badge">
              {backupData?.total_backups || 0} BACKUPS
            </span>

          </div>


          {!backupData ? (

            <div className="empty-state">

              <div className="check">
                ⌛
              </div>

              <h3>
                Loading Backup Information
              </h3>

              <p>
                Connecting to secure backup service.
              </p>

            </div>

          ) : (

            <div className="backup-content">

              <div className="backup-summary">

                <div className="backup-icon">
                  💾
                </div>

                <div>

                  <span>
                    Total Protected Backups
                  </span>

                  <h1>
                    {backupData.total_backups}
                  </h1>

                  <p>
                    Backup storage is active and ready
                    for recovery.
                  </p>

                </div>

              </div>


              <div className="backup-action">

                <h4>
                  Create Protected Backup
                </h4>

                <p>
                  Create a secure backup copy of the
                  protected demo file.
                </p>

                <button
                  className="backup-btn"
                  onClick={handleCreateBackup}
                  disabled={creatingBackup}
                >

                  {creatingBackup
                    ? "CREATING BACKUP..."
                    : "💾 CREATE BACKUP"}

                </button>

              </div>

            </div>

          )}


          {backupData?.backups?.length > 0 && (

            <div className="backup-list">

              <h4>
                Recent Backups
              </h4>

              {backupData.backups
                .slice(-3)
                .reverse()
                .map((backup, index) => (

                  <div
                    className="backup-item"
                    key={index}
                  >

                    <div>

                      <strong>
                        📄 {backup.name}
                      </strong>

                      <small>
                        Created: {backup.created_at}
                      </small>

                    </div>


                    <div className="backup-meta">

                      <span>
                        {backup.size} bytes
                      </span>

                      <span className="safe-badge">
                        SECURE
                      </span>

                    </div>

                  </div>

                ))}

            </div>

          )}

        </section>


        {/* ================= THREAT ACTIVITY TIMELINE ================= */}

        <section
          className="panel timeline-panel"
          id="timeline"
        >

          <div className="suspicious-header">

            <h3>
              📈 Threat Activity Timeline
            </h3>

            <span className="safe-badge">
              {timelineData.length} EVENTS
            </span>

          </div>


          {timelineData.length === 0 ? (

            <div className="empty-state">

              <div className="check">
                ✓
              </div>

              <h3>
                No Security Events
              </h3>

              <p>
                System activity will appear here.
              </p>

            </div>

          ) : (

            <div className="timeline-container">

              {timelineData.map((event) => (

                <div
                  className="timeline-item"
                  key={event.id}
                >

                  <div
                    className={
                      event.severity === "CRITICAL"
                        ? "timeline-dot critical"
                        : event.severity === "HIGH"
                        ? "timeline-dot high"
                        : "timeline-dot normal"
                    }
                  ></div>


                  <div className="timeline-content">

                    <div className="timeline-top">

                      <h4>
                        {event.title}
                      </h4>

                      <span
                        className={
                          event.severity === "CRITICAL"
                            ? "danger-badge"
                            : event.severity === "HIGH"
                            ? "high-badge"
                            : "safe-badge"
                        }
                      >
                        {event.severity}
                      </span>

                    </div>


                    <p>
                      {event.action}
                    </p>


                    <div className="timeline-meta">

                      <span>
                        🖥️ {event.process}
                      </span>

                      <span>
                        🕒 {event.timestamp}
                      </span>

                      <span>
                        ✓ {event.status}
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