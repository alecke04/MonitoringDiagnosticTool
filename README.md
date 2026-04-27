# Cloud-Based Web Server Monitoring & Diagnostics Tool

A self-contained monitoring and diagnostics tool that provides routine health checks for cloud-based web servers (Google Cloud, AWS, Azure). When downtime or SSL issues are detected, the tool generates an encrypted diagnostic report and sends an email notification to the server owner within 24 hours.

---

## How to Install
1. `python -m venv .venv`
2. `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux/macOS)
3. `pip install -r requirements.txt`

## How to Run
1. Complete the installation steps above
2. Activate the virtual environment: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux/macOS)
3. Execute: `python src/main.py run_test` to run the program (will trigger one monitoring cycle)
4. Execute: `python src/main.py generate_report` to send one report to the destination email adress

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
├── README.md                        # Project overview
├── requirements.txt                 # Python dependencies (auto-generated)
├── cron_setip.txt                   # Cron configuration file
│
├── docs/                            # Additional documentation
│   ├── setup_guide.md               # Setup and installation guide
│   ├── SRS.md                       # Software Requirements Specification
│   ├── SDS.md                       # Software Design Specification
│   ├── CHANGELOG.md                 # Revision history for SDS & SRS
│   └── requirements.txt             # Archived requirements reference
│
├── src/                             # Source code folder
│   ├── __init__.py
│   ├── main.py                      # Application entry point
│   │
│   ├── monitoring/                  # Monitoring module
│   │   ├── __init__.py
│   │   └── monitor.py               # MonitoringSystem class & availability checks
│   │
│   ├── notifications/               # Notification module
│   │   ├── __init__.py
│   │   ├── email_service.py         # Email sending via SMTP
│   │   └── report_generator_encrypt.py  # Report generation and encryption
│   │
│   ├── database/                    # Database module
│   │   ├── __init__.py
│   │   ├── db_class.py              # Abstract DbClass (base class)
│   │   ├── db_handle.py             # DatabaseHandle class (SQLite operations)
│   │   └── test_entry.py            # Test database entries
│   │
│   └── utils/                       # Utility functions
│       ├── __init__.py
│       └── analysis.py              # Data analysis utilities
│
├── diagrams/                        # Design diagrams (referenced in SDS/SRS)
│
├── data/                            # Runtime data (gitignored)
│   └── monitor.db                   # SQLite database (created at runtime)
│
├── reports/                         # Generated reports (gitignored)
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
   Create a `.env` file in the project root with your credentials:
   ```env
   GMAIL_SENDER=your-email@gmail.com
   GMAIL_SENDER_PASSWORD=your-app-password
   FILE_PASSWORD=your-report-archive-password
   ```

5. **Run the application:**
   ```bash
   python src/main.py --help
   ```

---

## Environment Variables

The application requires the following environment variables to be set in a `.env` file at the project root:

| Variable | Description | Example |
|---|---|---|
| `GMAIL_SENDER` | Gmail address for sending notifications | `your-email@gmail.com` |
| `GMAIL_SENDER_PASSWORD` | Gmail app-specific password | `abcd efgh ijkl mnop` |
| `FILE_PASSWORD` | Password for encrypting diagnostic reports | `SecurePassword123!` |

**Create `.env` file:**
```env
GMAIL_SENDER=your-email@gmail.com
GMAIL_SENDER_PASSWORD=your-app-password
FILE_PASSWORD=your-report-archive-password
```

> **Note:** Keep your `.env` file secure and never commit it to version control. The `.env` file is listed in `.gitignore`.

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
| [SRS.md](docs/SRS.md) | Software Requirements Specification — functional and nonfunctional requirements |
| [SDS.md](docs/SDS.md) | Software Design Specification — architecture, class diagrams, database design, algorithms |

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
