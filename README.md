# Cloud-Based Web Server Monitoring & Diagnostics Tool

A self-contained monitoring and diagnostics tool that provides routine health checks for cloud-based web servers (Google Cloud, AWS, Azure). When downtime or SSL issues are detected, the tool generates an encrypted diagnostic report and sends an email notification to the server owner within 24 hours.

---

## Features

- **Availability Monitoring** — Periodic HTTP/HTTPS checks to verify server reachability
- **RTT Performance Metrics** — Measures round-trip time over 100 requests; calculates average and median
- **SSL Certificate Validation** — Detects expired or invalid SSL certificates
- **Error Detection & Classification** — Identifies and categorizes HTTP errors and connection failures
- **Encrypted Reporting** — Generates AES-256 encrypted, password-protected diagnostic reports
- **Email Notifications** — Sends SMTP alerts with encrypted report attachments within 24 hours of failure detection
- **Persistent Storage** — SQLite database for historical monitoring data
- **Scheduled Execution** — Configurable monitoring intervals with automatic retry logic

---

## Project Structure

```
MonitoringDiagnosticTool/
│
├── README.md
├── docs/                             # Additional documentation
│   ├── setup_guide.md                   
│   ├── SRS.md                        # Software Requirements Specification
│   ├──SDS.md                         # Software Design Specification
│   ├── CHANGELOG.md                  # Revision history for SDS & SRS
│   ├── requirements.txt              # Python dependencies
│   └── .env.example                  # Example environment variables (SMTP credentials)
├── .gitignore                       
│
├── src/                             # Source code folder
│   ├── __init__.py
│   ├── main.py                      # Application entry point
│   ├── monitoring/                  # Monitoring module
│   │   ├── __init__.py
│   │   ├── monitor.py               # MonitoringSystem class
│   │   ├── availability.py          # Availability checking logic
│   │   ├── rtt.py                   # RTT measurement logic
│   │   └── ssl_check.py             # SSL certificate validation
│   │
│   ├── notifications/               # Notification module
│   │   ├── __init__.py
│   │   ├── email_service.py         # Email sending via SMTP
│   │   └── report_generator.py      # Report generation and encryption
│   │
│   ├── database/                    # Database module
│   │   ├── __init__.py
│   │   ├── db_handle.py             # DatabaseHandle class (SQLite operations)
│   │   └── schema.sql               # Database schema definition
│   │
│   ├── models/                      # Data models
│   │   ├── __init__.py
│   │   ├── web_server.py            # WebServer model
│   │   ├── monitor_run.py           # MonitorRun model
│   │   ├── monitor_history.py       # MonitorHistory model
│   │   └── results.py               # AvailResult, RTTResult, SSLResult
│   │
│   └── utils/                       # Utility functions
│       ├── __init__.py
│       ├── config.py                # Configuration loader
│       └── encryption.py            # AES-256 encryption utilities
│
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── test_availability.py         # Availability monitoring tests
│   ├── test_rtt.py                  # RTT measurement tests
│   ├── test_ssl.py                  # SSL validation tests
│   ├── test_database.py             # Database operation tests
│   ├── test_notifications.py        # Email and report tests
│   └── test_integration.py          # End-to-end integration tests
│
├── diagrams/                        # Design diagrams (referenced in SDS/SRS)
│   ├── architecture_diagram.png     # System architecture diagram
│   ├── class_diagram.png            # UML class diagram
│   ├── activity_diagram.png         # Activity flow diagram
│   ├── use_case_diagram.png         # Use case diagram
│   └── database_erd.png             # Entity-Relationship Diagram
│
├── data/                            # Runtime data (gitignored)
│   └── monitor.db                   # SQLite database (created at runtime)
│
├── reports/                         # Generated reports (gitignored)
│   └── .gitkeep
│
├── docs/                            # Additional documentation
│   └── setup_guide.md               
│
└── documentation_logs/              # Team work logs
    ├── Alec/
    ├── Jacob/
    ├── Natasha/
    └── Pjark/
```

---

## Requirements

- **Python 3.10+**
- **SQLite 3** (bundled with Python)
- **Internet connectivity** for monitoring and email delivery
- **SMTP-compatible email account** 

**Supported Operating Systems:**
- Windows 10/11
- Ubuntu 22.04 LTS or later

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/alecke04/MonitoringDiagnosticTool.git
   cd MonitoringDiagnosticTool
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux/macOS
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your SMTP credentials and report password:
   ```env
   SMTP_EMAIL=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   REPORT_PASSWORD=your-report-archive-password
   ```

5. **Initialize the database:**
   ```bash
   python src/main.py --init-db
   ```

---

## Usage

### Add a server to monitor

```bash
python src/main.py add https://example.com admin@example.com
```

### List monitored servers

```bash
python src/main.py list
```

### Start monitoring

```bash
python src/main.py start
```

### View server status

```bash
python src/main.py status 1
```

### View monitoring history

```bash
python src/main.py history 1 --from 2026-01-01 --to 2026-03-01
```

---

## Architecture Overview

The system follows a **client-server architecture**:

| Component | Description |
|---|---|
| **Host Machine** | Runs the monitoring tool; sends HTTP requests and SMTP emails |
| **Web Server** | The monitored target; responds to HTTP GET requests |
| **Email Server** | Relays encrypted diagnostic reports to the server owner |

All monitoring data is stored locally in an SQLite database. When a failure is detected, the system generates an AES-256 encrypted report and delivers it via SMTP within 24 hours.

---

## Documentation

| Document | Description |
|---|---|
| [SRS.md](SRS.md) | Software Requirements Specification — functional and nonfunctional requirements |
| [SDS.md](SDS.md) | Software Design Specification — architecture, class diagrams, database design, algorithms |

---

## Technologies

| Technology | Purpose |
|---|---|
| **Python 3** | Core programming language |
| **SQLite 3** | Embedded database for monitoring history |
| **SMTP (TLS)** | Secure email delivery |
| **AES-256** | Report encryption |
| **HTTP/2 + TLS 1.3** | Secure web server communication |

---

## Authors

- Alec Brenes
- Jacob Hensley
- Natasha Linares
- Pjark Sander

**Florida Polytechnic University** — Spring 2026

---

## License

This project is developed for academic purposes at Florida Polytechnic University.
