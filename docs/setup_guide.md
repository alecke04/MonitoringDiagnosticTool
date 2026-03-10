# Setup Guide — Monitoring and Diagnostics Tool

## Overview

This guide walks through cloning, configuring, and running the tool on Windows or Ubuntu.

---

## Prerequisites

- Python 3.10+
- SQLite 3 (bundled with Python — no separate install needed)
- An SMTP-compatible email account (e.g. Gmail with an App Password)
- Internet connectivity

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/alecke04/MonitoringDiagnosticTool.git
cd MonitoringDiagnosticTool
```

---

## Step 2: Create a Virtual Environment

```bash
python -m venv venv

# Activate (Windows):
venv\Scripts\activate

# Activate (Linux/macOS):
source venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r docs/requirements.txt
```

---

## Step 4: Configure Environment Variables

```bash
cp docs/.env.example .env
```

Open `.env` and fill in your credentials:

```env
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
REPORT_PASSWORD=your-archive-password
DB_PATH=data/monitor.db
TIMEOUT=10
RETRY_DELAY=5
MAX_RETRIES=3
```

> **Gmail users:** Generate an App Password at myaccount.google.com → Security → App Passwords.

---

## Step 5: Initialize the Database

```bash
python src/main.py --init-db
```

This creates `data/monitor.db` with all required tables.

---

## Step 6: Add a Server to Monitor

```bash
python src/main.py add https://example.com admin@example.com
```

---

## Step 7: Start Monitoring

```bash
python src/main.py start
```

The tool will run in the foreground, checking all registered servers on their configured intervals.

---

## Common Commands

| Command | Description |
|---|---|
| `python src/main.py list` | List all monitored servers |
| `python src/main.py status <id>` | Show latest result for a server |
| `python src/main.py history <id>` | Show full history for a server |
| `python src/main.py remove <id>` | Remove a server from monitoring |

---

## Troubleshooting

<!-- TODO: add common error messages and solutions here as the team encounters them -->
