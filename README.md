# RansomTrap

RansomTrap is a Windows-first ransomware detection, containment, forensic logging, and recovery prototype.

The project uses decoy/trap files, filesystem monitoring, entropy-based detection, process inspection, local recovery snapshots, and SQLite logging.

The security agent is designed to work independently from the dashboard.

---

## 1. Project Architecture

```text
                    RANSOMTRAP
                        |
            +-----------+-----------+
            |                       |
       Security Agent           Dashboard
            |                       |
            |                    Flask API
            |                       |
            +---- SQLite ----------+
                   |
              React UI