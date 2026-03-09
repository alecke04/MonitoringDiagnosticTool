# Software Design Specification

## Monitoring and Diagnostics Tool for Cloud-Based Web Servers

**Version 1.0**

| | |
|---|---|
| **Authors** | Alec Brenes, Jacob Hensley, Natasha Linares, Pjark Sander |
| **Institution** | Florida Polytechnic University |
| **Date** | February 26, 2026 |

---

## Table of Contents

1. [Introduction](#1-introduction)
   - 1.1 [Purpose](#11-purpose)
   - 1.2 [System Overview](#12-system-overview)
2. [Design Considerations](#2-design-considerations)
   - 2.1 [Assumptions](#21-assumptions)
   - 2.2 [General Constraints](#22-general-constraints)
3. [System Architecture](#3-system-architecture)
4. [Detailed System Design](#4-detailed-system-design)
   - 4.1 [Class Diagram](#41-class-diagram)
   - 4.2 [Activity Diagram](#42-activity-diagram)
   - 4.3 [Sequence Diagram](#43-sequence-diagram)
   - 4.4 [State Chart Diagram](#44-state-chart-diagram)
   - 4.5 [Algorithms for Components/Methods](#45-algorithms-for-componentsmethods)
5. [Database Design](#5-database-design)
   - 5.1 [Table Definitions](#51-table-definitions)
   - 5.2 [Relationships](#52-relationships)
   - 5.3 [Keys and Constraints](#53-keys-and-constraints)
6. [User Interface Design](#6-user-interface-design)
7. [Appendix A: Glossary](#appendix-a-glossary)

---

## 1. Introduction

### 1.1 Purpose

The purpose of this document is to outline the design details of the Monitoring and Diagnostics Tool for cloud-based web servers. It covers the system's design requirements including database schema, constraints, and system architecture details conveyed via diagrams.

### 1.2 System Overview

This system is an independent tool that provides routine monitoring of specified web servers running on platforms such as Google Cloud or AWS. If the system detects downtime or SSL issues, it produces a diagnostic report and sends an email notification with a password-protected encrypted archive file attached, within 24 hours of detection. When servers are healthy, the system computes performance metrics including average and median Round-Trip Time (RTT) to retrieve a sample synthetic payload.

---

## 2. Design Considerations

### 2.1 Assumptions

This system assumes the following requirements and dependencies are met:

**Software/Hardware Requirements:**
- Python 3 runtime is available
- SQLite 3 is available as an embedded database
- SMTP-compatible email provider is accessible
- Host machine supports TLS 1.2+ connections

**Operating System Dependencies:**
- Windows 10/11
- Ubuntu 22.04 LTS or later

**End-User Characteristics:**
- Basic command-line knowledge
- SMTP credential configuration knowledge
- Administrative access to host system

### 2.2 General Constraints

**Hardware Constraints:**
- Service runs on standard host hardware
- No specialized hardware required
- Performance limited by CPU, memory, and network bandwidth

**Software Constraints:**
- Must operate using Python standard libraries and approved third-party packages
- Uses SQLite (no centralized DB server)
- Uses SMTP over TLS for email delivery

**Software Compliance:**
- HTTP/2
- TLS 1.3
- SMTP over TLS (STARTTLS)

**Security Constraints:**
- Email encryption via AES-256
- Password protection on report archive files

---

## 3. System Architecture

![System Architecture Diagram](diagrams/architecture_diagram.png)

The system architecture follows a **client-server style** and is designed around the functions and tasks that the system executes. The structure depends on the connections between the client's host machine, the monitored web server, and the server owner's email.

| Component | Role |
|---|---|
| **System Host Machine** | Runs the monitoring tool; initiates HTTP requests and sends SMTP emails |
| **Web Server** | The monitored target; receives HTTP GET requests and returns HTTP responses |
| **Email Server** | Relays SMTP notifications from the host machine to the server owner |
| **Server Owner** | Receives email notifications containing encrypted diagnostic reports |
| **Internet** | Network medium connecting all components via HTTP and SMTP protocols |

Both the system host machine and the server owner access the web server and email server via an internet connection. The host machine sends HTTP GET requests to the web server and receives HTTP responses. When a failure is detected, the host machine sends encrypted diagnostic reports via SMTP to the email server, which delivers the notification to the server owner.

---

## 4. Detailed System Design

### 4.1 Class Diagram

![Class Diagram](diagrams/class_diagram.png)

The system consists of the following classes and their relationships:

#### `WebServer`

Represents a monitored web server target.

| Attribute | Type | Description |
|---|---|---|
| `id` | `int` | Unique identifier for the server |
| `url` | `str` | Target server URL |
| `email` | `str` | Server owner's email address |
| `sample` | `str` | Path to the synthetic payload for RTT measurement |

#### `MonitoringSystem`

Core class that orchestrates all monitoring tasks.

| Attribute | Type | Description |
|---|---|---|
| `timeoutDuration` | `int` | Maximum wait time for server responses (seconds) |
| `retryDelayMinutes` | `int` | Delay between retries (default: 5) |
| `maxRetries` | `int` | Maximum number of retry attempts |

| Method | Return Type | Description |
|---|---|---|
| `runCheck()` | `void` | Initiates a full monitoring cycle for all servers |
| `checkAvailability(server: WebServer)` | `AvailResult` | Checks if the server is reachable and returns HTTP status |
| `measureRTT(server: WebServer, samples: int = 100)` | `RTTResult` | Measures RTT over multiple requests |
| `checkSSL(server: WebServer)` | `SSLResult` | Validates the server's SSL certificate |
| `waitRetryAvailability(server: WebServer)` | `AvailResult` | Retries availability checks with increased frequency |
| `generateSendReport(server: WebServer, failure: AvailResult)` | `void` | Generates a diagnostic report and triggers notification |

#### `NotificationService`

Handles report generation, encryption, and email delivery.

| Attribute | Type | Description |
|---|---|---|
| `reportPassword` | `str` | Password used for encrypting report archives |
| `senderEmail` | `str` | Email address used to send notifications |
| `senderPassword` | `str` | SMTP credentials for the sender account |

| Method | Return Type | Description |
|---|---|---|
| `notifyFailure(server, history, failure)` | `void` | Builds and sends a failure notification |
| `buildReport(server, history, failure)` | `str` | Compiles diagnostic data into a structured report |
| `encryptReport(reportPath: str)` | `str` | Encrypts the report into a password-protected archive |
| `sendEmail(to, subject, body, attachmentPath)` | `void` | Sends the email with the encrypted attachment |

#### `MonitorHistory`

Maintains historical monitoring data for a specific target.

| Attribute | Type | Description |
|---|---|---|
| `targetId` | `int` | References the monitored server |
| `url` | `str` | Server URL |
| `emailRecipient` | `str` | Notification recipient |
| `startTime` | `str` | Start of the monitoring window |
| `endTime` | `str` | End of the monitoring window |
| `runs` | `list` | Collection of `MonitorRun` objects |

| Method | Return Type | Description |
|---|---|---|
| `getRuns(targetId, startTime, endTime)` | `list` | Retrieves runs within a time range |
| `addRun(run: MonitorRun)` | `void` | Appends a new run to history |
| `getFailureRuns()` | `list` | Filters runs where failures occurred |
| `summarizeRuns()` | `str` | Generates a summary of all runs |

#### `MonitorRun`

Represents a single monitoring cycle result.

| Attribute | Type | Description |
|---|---|---|
| `runId` | `int` | Unique run identifier |
| `timestamp` | `str` | Date/time of the monitoring run |
| `reachable` | `bool` | Whether the server was reachable |
| `httpStatus` | `int` | HTTP response code |
| `errorDescription` | `str` | Description of any error detected |
| `sslValid` | `bool` | Whether the SSL certificate is valid |
| `sslExpirationDate` | `str` | SSL certificate expiration date |
| `avgRTTms` | `float` | Average RTT in milliseconds |
| `medianRTTms` | `float` | Median RTT in milliseconds |
| `confidence90Interval` | `tuple` | 90% confidence interval for RTT |

#### `DatabaseHandle`

Manages all SQLite database operations.

| Attribute | Type | Description |
|---|---|---|
| `dbPath` | `str` | File path to the SQLite database |

| Method | Return Type | Description |
|---|---|---|
| `saveResult(server, availability, rtt, ssl)` | `int` | Persists a complete monitoring result; returns the run ID |
| `getRecent(number: int, server: WebServer)` | `list` | Retrieves the most recent N runs for a server |
| `getRunsInTimeframe(server, start, end)` | `list` | Retrieves runs within a date range |
| `updateNotificationStatus(runId, status)` | `void` | Updates the notification status for a run |

#### `AvailResult`

Data class for availability check results.

| Attribute | Type | Description |
|---|---|---|
| `isUp` | `bool` | Whether the server is up |
| `httpCode` | `int` | HTTP status code |
| `httpDescript` | `str` | HTTP status description |

#### `RTTResult`

Data class for round-trip time measurement results.

| Attribute | Type | Description |
|---|---|---|
| `count` | `int` | Number of measurements taken |
| `measurements` | `list` | List of individual RTT values |
| `average` | `float` | Calculated average RTT |
| `median` | `float` | Calculated median RTT |
| `confidence90Interval` | `tuple` | 90% confidence interval |

| Method | Return Type | Description |
|---|---|---|
| `calculateConfidenceInterval()` | `void` | Computes the 90% confidence interval from measurements |

#### `SSLResult`

Data class for SSL certificate validation results.

| Attribute | Type | Description |
|---|---|---|
| `isValid` | `bool` | Whether the certificate is valid |
| `expirationDate` | `str` | Certificate expiration date |

#### Class Relationships

| Relationship | Type | Description |
|---|---|---|
| `WebServer` → `MonitoringSystem` | 1 to 1 | Each server is monitored by the system |
| `MonitoringSystem` → `NotificationService` | 1 to 1 | The system triggers notifications |
| `MonitoringSystem` → `DatabaseHandle` | 1 to 1 | The system stores results via the database handle |
| `MonitoringSystem` → `AvailResult` | 1 to 0..1 | A check generates an availability result |
| `MonitoringSystem` → `RTTResult` | 1 to 0..1 | A check generates an RTT result |
| `MonitoringSystem` → `SSLResult` | 1 to 0..1 | A check generates an SSL result |
| `MonitorHistory` → `MonitorRun` | 1 to 1..* | A history holds one or more runs (composition) |
| `DatabaseHandle` → `MonitorHistory` | 1 to 0..* | The database retrieves historical data |
| `NotificationService` → `MonitorHistory` | 1 to 1 | Notifications reference monitoring history for report generation |

---

### 4.2 Activity Diagram

![Activity Diagram](diagrams/activity_diagram.png)

This diagram illustrates the activity flow of the monitoring system at runtime:

1. **Launch Application** — The system starts and begins operating in the background on the host machine.
2. **Can Connect to Server?** — The system attempts to connect to the target web server.
   - **Yes → Run Diagnostics** — If the server is reachable, the system performs a full diagnostic cycle (availability check, RTT measurement, SSL validation).
   - **No → Increase Monitoring Frequency** — If the server is unreachable, the system increases the monitoring frequency and retries.
3. **Diagnostic Results** — After diagnostics complete, the system evaluates the results.
   - **Error Found → Send Encrypted Email** — If an issue is detected (HTTP error, SSL expiration, etc.), the system generates an encrypted report and sends it via email to the server owner. The application then ends the current notification cycle.
   - **No Error → Continue Monitoring** — If no issues are found, the system continues routine monitoring.
4. **Retry Path** — After increasing monitoring frequency:
   - **Can Connect to Server? (Yes)** — The system proceeds to run diagnostics.
   - **Can Connect to Server? (No)** — A persistent failure triggers a **404 Error** classification, and the system sends an encrypted email notification.

---

### 4.3 Sequence Diagram

#### Scenario 1: Successful Monitoring Cycle (No Errors)

```
Host Machine          MonitoringSystem        WebServer        DatabaseHandle
     |                      |                    |                   |
     |--- runCheck() ------>|                    |                   |
     |                      |-- HTTP GET ------->|                   |
     |                      |<-- 200 OK ---------|                   |
     |                      |                    |                   |
     |                      |-- measureRTT() --->|                   |
     |                      |  (100 requests)    |                   |
     |                      |<-- RTT data -------|                   |
     |                      |                    |                   |
     |                      |-- checkSSL() ----->|                   |
     |                      |<-- SSL valid ------|                   |
     |                      |                    |                   |
     |                      |-- saveResult() ------------------->|  |
     |                      |<-- run ID -------------------------|  |
     |                      |                    |                   |
     |<-- cycle complete ---|                    |                   |
```

The system initiates a monitoring cycle by sending an HTTP GET request to the web server. Upon receiving a `200 OK` response, it performs 100 RTT measurements and validates the SSL certificate. All results are persisted to the SQLite database. No notification is triggered since no errors were found.

#### Scenario 2: Server Down — Failure Notification Flow

```
Host Machine     MonitoringSystem     WebServer     DatabaseHandle     NotificationService     EmailServer
     |                 |                 |                |                    |                    |
     |-- runCheck() -->|                 |                |                    |                    |
     |                 |-- HTTP GET ---->|                |                    |                    |
     |                 |<-- timeout -----|                |                    |                    |
     |                 |                 |                |                    |                    |
     |                 |-- waitRetry() ->|                |                    |                    |
     |                 |<-- timeout -----|                |                    |                    |
     |                 |                 |                |                    |                    |
     |                 |-- saveResult() ------------>|   |                    |                    |
     |                 |<-- run ID ------------------|   |                    |                    |
     |                 |                 |                |                    |                    |
     |                 |-- generateSendReport() -------->|                    |                    |
     |                 |                 |                | -- buildReport() ->|                    |
     |                 |                 |                |                    |-- encryptReport() -|
     |                 |                 |                |                    |-- sendEmail() ---->|
     |                 |                 |                |                    |<-- SMTP OK --------|
     |                 |                 |                |                    |                    |
     |                 |                 |                |<-- updateStatus() -|                    |
     |<-- complete ----|                 |                |                    |                    |
```

When the server is unreachable, the system retries with increased frequency. After exhausting retries, it logs the failure to the database, generates an encrypted diagnostic report, and sends it via SMTP to the server owner. The notification status is updated in the database.

---

### 4.4 State Chart Diagram

The following state chart describes the lifecycle of a monitored web server from the system's perspective:

```
                    ┌─────────────┐
                    │    IDLE     │
                    └──────┬──────┘
                           │ timer triggers monitoring cycle
                           ▼
                    ┌─────────────┐
            ┌──────│  CHECKING   │──────┐
            │      └─────────────┘      │
        reachable               unreachable
            │                           │
            ▼                           ▼
    ┌───────────────┐         ┌─────────────────┐
    │  DIAGNOSING   │         │    RETRYING      │
    └───────┬───────┘         └────────┬────────┘
            │                          │
      ┌─────┴─────┐            ┌──────┴──────┐
   no error     error       connected     max retries
      │           │             │          exceeded
      ▼           ▼             ▼             │
 ┌─────────┐ ┌──────────┐ ┌───────────┐      │
 │ HEALTHY │ │ ALERTING │ │ DIAGNOSING│      │
 └────┬────┘ └─────┬────┘ └───────────┘      │
      │            │                          ▼
      │            ▼                   ┌──────────┐
      │      ┌───────────┐            │ ALERTING │
      │      │ NOTIFIED  │            └─────┬────┘
      │      └─────┬─────┘                  │
      │            │                        ▼
      │            │                  ┌───────────┐
      └────────────┴─────────────────►│   IDLE    │
                 reset timer          └───────────┘
```

**States:**

| State | Description |
|---|---|
| **IDLE** | System is waiting for the next scheduled monitoring cycle |
| **CHECKING** | System is attempting to connect to the web server |
| **DIAGNOSING** | System is performing full diagnostics (RTT, SSL) |
| **RETRYING** | System is retrying connection with increased frequency |
| **HEALTHY** | Server passed all diagnostic checks |
| **ALERTING** | System is generating the report and preparing notification |
| **NOTIFIED** | Encrypted email has been sent to the server owner |

---

### 4.5 Algorithms for Components/Methods

#### `MonitoringSystem.runCheck()`

```
PROCEDURE runCheck()
    FOR EACH server IN monitored_servers:
        availability ← checkAvailability(server)

        IF availability.isUp THEN
            rtt ← measureRTT(server, samples=100)
            ssl ← checkSSL(server)
            db.saveResult(server, availability, rtt, ssl)

            IF NOT ssl.isValid THEN
                generateSendReport(server, availability)
            END IF
        ELSE
            retryResult ← waitRetryAvailability(server)

            IF retryResult.isUp THEN
                rtt ← measureRTT(server, samples=100)
                ssl ← checkSSL(server)
                db.saveResult(server, retryResult, rtt, ssl)
            ELSE
                db.saveResult(server, retryResult, NULL, NULL)
                generateSendReport(server, retryResult)
            END IF
        END IF
    END FOR
END PROCEDURE
```

#### `MonitoringSystem.checkAvailability(server)`

```
PROCEDURE checkAvailability(server: WebServer) → AvailResult
    TRY
        response ← HTTP_GET(server.url, timeout=timeoutDuration)
        RETURN AvailResult(
            isUp = (response.status_code < 400),
            httpCode = response.status_code,
            httpDescript = response.reason
        )
    CATCH TimeoutError
        RETURN AvailResult(isUp=FALSE, httpCode=0, httpDescript="Connection timed out")
    CATCH ConnectionError
        RETURN AvailResult(isUp=FALSE, httpCode=0, httpDescript="Connection refused")
    END TRY
END PROCEDURE
```

#### `MonitoringSystem.measureRTT(server, samples)`

```
PROCEDURE measureRTT(server: WebServer, samples: int = 100) → RTTResult
    measurements ← empty list

    FOR i FROM 1 TO samples:
        startTime ← current_time_ms()
        HTTP_GET(server.url + server.sample)
        endTime ← current_time_ms()
        rtt ← endTime - startTime
        APPEND rtt TO measurements
    END FOR

    average ← SUM(measurements) / LENGTH(measurements)
    sorted ← SORT(measurements)
    median ← sorted[LENGTH(sorted) / 2]

    result ← RTTResult(count=samples, measurements, average, median)
    result.calculateConfidenceInterval()
    RETURN result
END PROCEDURE
```

#### `MonitoringSystem.checkSSL(server)`

```
PROCEDURE checkSSL(server: WebServer) → SSLResult
    TRY
        cert ← TLS_GET_CERTIFICATE(server.url)
        expirationDate ← cert.notAfter
        isValid ← (expirationDate > CURRENT_DATE)
        RETURN SSLResult(isValid=isValid, expirationDate=expirationDate)
    CATCH SSLError
        RETURN SSLResult(isValid=FALSE, expirationDate="Unknown")
    END TRY
END PROCEDURE
```

#### `MonitoringSystem.waitRetryAvailability(server)`

```
PROCEDURE waitRetryAvailability(server: WebServer) → AvailResult
    FOR attempt FROM 1 TO maxRetries:
        WAIT(retryDelayMinutes * 60 seconds)
        result ← checkAvailability(server)
        IF result.isUp THEN
            RETURN result
        END IF
    END FOR
    RETURN AvailResult(isUp=FALSE, httpCode=404, httpDescript="Server unreachable after retries")
END PROCEDURE
```

#### `NotificationService.notifyFailure(server, history, failure)`

```
PROCEDURE notifyFailure(server: WebServer, history: MonitorHistory, failure: AvailResult)
    reportContent ← buildReport(server, history, failure)
    reportPath ← SAVE_TO_FILE(reportContent)
    encryptedPath ← encryptReport(reportPath)

    subject ← "ALERT: Server Issue Detected — " + server.url
    body ← "A failure has been detected on " + server.url + ". See attached report."

    sendEmail(
        to = server.email,
        subject = subject,
        body = body,
        attachmentPath = encryptedPath
    )
END PROCEDURE
```

#### `NotificationService.encryptReport(reportPath)`

```
PROCEDURE encryptReport(reportPath: str) → str
    archivePath ← reportPath + ".zip"
    CREATE_ZIP_ARCHIVE(archivePath, files=[reportPath], password=reportPassword, encryption=AES-256)
    DELETE(reportPath)
    RETURN archivePath
END PROCEDURE
```

#### `DatabaseHandle.saveResult(server, availability, rtt, ssl)`

```
PROCEDURE saveResult(server: WebServer, availability: AvailResult, rtt: RTTResult, ssl: SSLResult) → int
    INSERT INTO monitored_runs (
        target_id = server.id,
        timestamp = CURRENT_TIMESTAMP,
        reachable = availability.isUp,
        http_status = availability.httpCode,
        error_code = availability.httpDescript,
        ssl_expiration = ssl.expirationDate (IF ssl IS NOT NULL),
        avg_rtt = rtt.average (IF rtt IS NOT NULL),
        median_rtt = rtt.median (IF rtt IS NOT NULL)
    )
    runId ← LAST_INSERT_ID()

    IF rtt IS NOT NULL THEN
        FOR i FROM 1 TO LENGTH(rtt.measurements):
            INSERT INTO rtt_samples (run_id=runId, rtt_value=rtt.measurements[i])
        END FOR
    END IF

    RETURN runId
END PROCEDURE
```

---

## 5. Database Design

![Database ERD](diagrams/database_erd.png)

### 5.1 Table Definitions

#### Table 1: `monitored_targets`

Stores configuration for each monitored server.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `target_id` | `INTEGER` | **PK**, `AUTO INCREMENT` | Unique identifier for each monitored target |
| `url` | `TEXT` | `UNIQUE`, `NOT NULL`, **AK** | Target server URL to monitor |
| `sample_path` | `TEXT` | `NOT NULL` | Path to the 1 KB synthetic payload |
| `email_recipient` | `TEXT` | `NOT NULL` | Email address that receives alerts/reports |
| `interval` | `INTEGER` | `NOT NULL` | Monitoring interval (in seconds) |
| `timeout` | `INTEGER` | `NOT NULL` | Request timeout value (in seconds) |
| `retry_count` | `INTEGER` | `NOT NULL` | Number of retry attempts before marking "Down" |

#### Table 2: `monitored_runs`

Stores results of each monitoring cycle for each target.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `run_id` | `INTEGER` | **PK**, `AUTO INCREMENT` | Unique identifier for each monitoring cycle |
| `target_id` | `INTEGER` | **FK** → `monitored_targets(target_id)` | References the monitored target |
| `timestamp` | `TEXT` | `NOT NULL` | Date/time of the run (ISO 8601 with timezone) |
| `reachable` | `INTEGER` | `NOT NULL` | Boolean indicator of server reachability (0/1) |
| `http_status` | `INTEGER` | | HTTP response code |
| `error_code` | `TEXT` | | Standardized error label |
| `ssl_expiration` | `TEXT` | | Certificate expiration status/date |
| `avg_rtt` | `REAL` | `CHECK(avg_rtt >= 0)` | Average RTT from 100 request measurements (ms) |
| `median_rtt` | `REAL` | `CHECK(median_rtt >= 0)` | Median RTT from 100 request measurements (ms) |

#### Table 3: `rtt_samples`

Stores individual RTT measurements for each monitoring run.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `sample_id` | `INTEGER` | **PK**, `AUTO INCREMENT` | Unique identifier for each sample |
| `run_id` | `INTEGER` | **FK** → `monitored_runs(run_id)` | References the monitoring run |
| `rtt_value` | `REAL` | `NOT NULL`, `CHECK(rtt_value >= 0)` | Individual RTT measurement (ms) |

#### Table 4: `notifications`

Stores email notification logs tied to monitoring runs.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `notification_id` | `INTEGER` | **PK**, `AUTO INCREMENT` | Unique identifier for a notification event |
| `run_id` | `INTEGER` | **FK** → `monitored_runs(run_id)` | References the monitoring run |
| `sent_status` | `TEXT` | `CHECK(sent_status IN ('PENDING','SENT','FAILED'))` | Notification delivery status |
| `filename` | `TEXT` | | Encrypted archive filename attached to email |
| `time_sent` | `TEXT` | | Timestamp when email was sent (ISO 8601) |

### 5.2 Relationships

| Relationship | Cardinality | Description |
|---|---|---|
| `monitored_targets` → `monitored_runs` | 1 : N | One target can have many monitoring runs |
| `monitored_runs` → `rtt_samples` | 1 : N | One run generates up to 100 RTT samples |
| `monitored_runs` → `notifications` | 1 : 0..1 | One run can generate zero or one notification |

### 5.3 Keys and Constraints

**Primary Keys:**
- `monitored_targets.target_id`
- `monitored_runs.run_id`
- `rtt_samples.sample_id`
- `notifications.notification_id`

**Foreign Keys:**
- `monitored_runs.target_id` → `monitored_targets.target_id`
- `rtt_samples.run_id` → `monitored_runs.run_id`
- `notifications.run_id` → `monitored_runs.run_id`

**Alternate Keys:**
- `monitored_targets.url` is unique

**Integrity Constraints:**
- `url` must be unique and non-null
- `rtt_value` must be non-negative
- `sent_status` must be one of `{PENDING, SENT, FAILED}`
- `avg_rtt` and `median_rtt` must be non-negative

---

## 6. User Interface Design

The user interface is a **terminal-based (CLI) application**. The user interacts with the system through the command line to configure target servers and view monitoring status.

**Key UI Interactions:**

| Command | Description |
|---|---|
| `add <url> <email>` | Adds a new web server to the monitoring list |
| `remove <id>` | Removes a server from the monitoring list |
| `list` | Displays all currently monitored servers |
| `status <id>` | Shows the latest monitoring result for a server |
| `history <id> [--from DATE] [--to DATE]` | Displays historical monitoring data |
| `start` | Begins the monitoring loop |
| `stop` | Stops the monitoring loop |

**Example Terminal Output:**

```
$ python monitor.py list
┌────┬─────────────────────────┬──────────────────────┬──────────┐
│ ID │ URL                     │ Email                │ Status   │
├────┼─────────────────────────┼──────────────────────┼──────────┤
│  1 │ https://example.com     │ admin@example.com    │ Healthy  │
│  2 │ https://myserver.io     │ owner@myserver.io    │ Down     │
└────┴─────────────────────────┴──────────────────────┴──────────┘
```

---

## Appendix A: Glossary

| Term | Definition |
|---|---|
| **RTT** | Round-Trip Time — time for a data packet to travel from source to destination and back, measured in milliseconds |
| **HTTP** | Hypertext Transfer Protocol — foundational application-layer protocol for web communication |
| **HTTPS** | HTTP Secure — HTTP over TLS for encrypted communication |
| **SSL** | Secure Sockets Layer — protocol for encrypting data between web server and client |
| **TLS** | Transport Layer Security — successor to SSL; provides encryption and data integrity |
| **SMTP** | Simple Mail Transfer Protocol — standard protocol for sending email |
| **SQLite** | Lightweight, serverless, embedded relational database engine |
| **AES-256** | Advanced Encryption Standard with 256-bit key — industry-standard encryption algorithm |
| **CLI** | Command-Line Interface — text-based interface for interacting with the application |
| **PK** | Primary Key — unique identifier for a database record |
| **FK** | Foreign Key — reference to a primary key in another table |
| **ERD** | Entity-Relationship Diagram — visual representation of database structure |








