# Software Requirements Specification

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
   - 1.2 [Intended Audience and Reading Suggestions](#12-intended-audience-and-reading-suggestions)
   - 1.3 [Product Scope](#13-product-scope)
2. [Overall Description](#2-overall-description)
   - 2.1 [Product Perspective](#21-product-perspective)
   - 2.2 [Product Functions](#22-product-functions)
   - 2.3 [User Classes and Characteristics](#23-user-classes-and-characteristics)
   - 2.4 [Operating Environment](#24-operating-environment)
   - 2.5 [Design and Implementation Constraints](#25-design-and-implementation-constraints)
   - 2.6 [User Documentation](#26-user-documentation)
   - 2.7 [Assumptions and Dependencies](#27-assumptions-and-dependencies)
3. [External Interface Requirements](#3-external-interface-requirements)
   - 3.1 [Hardware Interfaces](#31-hardware-interfaces)
   - 3.2 [Software Interfaces](#32-software-interfaces)
   - 3.3 [Communications Interfaces](#33-communications-interfaces)
4. [System Features](#4-system-features)
   - 4.1 [Web Server Availability Monitoring](#41-web-server-availability-monitoring)
   - 4.2 [Round-Trip Time Measurement](#42-round-trip-time-measurement)
   - 4.3 [SSL Certificate Expiration Monitoring](#43-ssl-certificate-expiration-monitoring)
   - 4.4 [Error Detection and Classification](#44-error-detection-and-classification)
   - 4.5 [Email Notification System](#45-email-notification-system)
   - 4.6 [Encrypted Report Generation](#46-encrypted-report-generation)
   - 4.7 [Persistent Data Storage (SQLite Database)](#47-persistent-data-storage-sqlite-database)
   - 4.8 [Scheduled Monitoring Execution](#48-scheduled-monitoring-execution)
5. [Other Nonfunctional Requirements](#5-other-nonfunctional-requirements)
   - 5.1 [Performance Requirements](#51-performance-requirements)
   - 5.2 [Safety Requirements](#52-safety-requirements)
   - 5.3 [Security Requirements](#53-security-requirements)
   - 5.4 [Software Quality Attributes](#54-software-quality-attributes)
6. [Other Requirements](#6-other-requirements)
7. [Analysis Models](#7-analysis-models)
8. [Appendix A: Glossary](#appendix-a-glossary)

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) defines the functional and nonfunctional requirements for the Cloud-Based Web Server Monitoring & Diagnostics Tool. The goal of the tool is to design and develop software to monitor the health of web servers hosted in the cloud, such as Google Cloud, Amazon EC2, or Microsoft Azure. This project will provide diagnostic data about a web server and will automatically notify the server owner, via email, if the server is down within 24 hours. The product will provide the error code and a brief description of the detected problem with the server. This SRS covers monitoring, diagnostics, documentation, and reporting details of the product.

### 1.2 Intended Audience and Reading Suggestions

The different types of readers that this document is intended for are project managers, developers, and IT analysts. This SRS contains product scope, description, and requirement specifications. The requirements include product functions, user classes and characteristics, operating environment, design constraints, user documentation, and assumptions and dependencies about the product. The SRS also covers external requirements (hardware, software, and communication interfaces), system features, and additional nonfunctional requirements including performance, safety, security, and quality attributes.

> **Recommended reading order:** Start with Sections 1–3 for context, then review Section 4 for detailed functional requirements, and Section 5 for nonfunctional requirements.

### 1.3 Product Scope

The tool provides routine monitoring of specified web servers running on platforms such as Google Cloud or AWS. In the event that the system detects downtime or SSL issues, it produces a diagnostic report and sends an email notification with a password-protected encrypted archive file attached, within 24 hours of detection. When servers are healthy, the system computes performance metrics including average and median Round-Trip Time (RTT) to retrieve a sample synthetic payload.

**Key benefits:**
- Faster incident awareness
- Improved uptime oversight
- Secure delivery of diagnostic data to server owners
- Real-time server diagnostics for internal use by private firms to ensure uptime and minimize profit loss during service disruptions

---

## 2. Overall Description

### 2.1 Product Perspective

Given that servers are naturally exposed to vulnerabilities in the current climate, this tool is intended to detect said vulnerabilities and notify the server's owner. The Monitoring and Diagnostic Tool is a self-contained application that is to be run from a host computer or deployed as a lightweight service. It interfaces with external web servers over HTTPS/HTTP and an email delivery provider (SMTP or API-based).

![System Context Diagram](diagrams/system_context_diagram.png)

### 2.2 Product Functions

The web server monitoring and diagnostic tool provides automated monitoring to ensure that cloud-based web servers remain accessible and reliable. The main features include:

| Feature | Description |
|---|---|
| **Web Server Availability Monitoring** | Periodically attempts to reach the target URL to determine accessibility. Documents incidents and notifies appropriate parties on failure. |
| **HTTP Error Code Diagnostic** | Documents HTTP errors with short descriptions and timestamps when availability issues occur. |
| **SSL Certificate Monitoring** | Monitors the status of SSL certificates for all targets. Notifies appropriate parties if a certificate has expired. |
| **RTT Performance Diagnostic** | Measures Round-Trip Time (RTT) at least 100 times using 1 KB of sample data. Calculates and records average and median RTT. |
| **Secure Report Generation** | Generates encrypted reports delivered to the web server owner/administrator. Reports include errors, descriptions, and timestamps. |
| **Email Delivery** | Creates password-protected files delivered to the client via SMTP within 24 hours of failure detection. |

### 2.3 User Classes and Characteristics

The system will primarily be used by three user classes:

| User Class | Responsibilities |
|---|---|
| **Server Administrator** | Responsible for installation, configuration, maintenance, and security of server infrastructure. Primarily receives email alerts containing diagnostic reports about the web server. |
| **IT Analyst** | Responsible for monitoring system architecture, including server connection status and uptime. Analyzes, designs, and implements computer systems and troubleshoots issues. |
| **Developer** | Responsible for engineering the system's architecture and functionality. |

### 2.4 Operating Environment

This software operates in a local environment within a local machine and is compatible with any Windows or Linux platform. It requires:

- Internet connectivity for availability checks and email reports
- Python 3 runtime environment
- SQLite for data storage

### 2.5 Design and Implementation Constraints

| Constraint Category | Details |
|---|---|
| **Cloud-Server Policies** | Must comply with acceptable-use and rate-limit policies of cloud providers (Google Cloud, Amazon EC2, Microsoft Azure). |
| **Hardware** | Runs on a standard host machine with limited CPU, memory, and internet bandwidth. Continuous internet connectivity is required. The cloud server must run in parallel with the local machine. |
| **Interface** | Terminal-based communication with the local machine. SQLite database for tracking error code deliveries. |
| **Timing** | Must provide a notification within 24 hours of the problem being detected, including time zone and date of occurrence. |
| **Technology** | Runs on a local machine; limited to the given storage and speed of the machine and the amount of monitoring possible. |
| **Security** | Email report files must be encrypted and password-protected; the local machine must be access-controlled. |
| **Maintenance** | Code must follow clear documentation and modular design practices. Utilizes Git version control. |

### 2.6 User Documentation

Users will have access to a `README.md` file which includes setup and usage instructions. The application runs in the background on the host machine and is designed to be simple to use for both beginner and experienced developers.

### 2.7 Assumptions and Dependencies

The system assumes the following:

- A continuous and stable internet connection is available to perform regular checks and send email reports.
- The configured email account is set up correctly and authorized to send messages via SMTP.
- The target web servers are properly configured and will respond to requests.
- The host machine is secure and will have access control enforced.

**Dependencies:**
- Python 3 runtime environment
- A properly configured Gmail address with valid credentials for SMTP
- SQLite database for storing performance data
- Encryption utility to create password-protected report files

---

## 3. External Interface Requirements

### 3.1 Hardware Interfaces

The monitoring and diagnostic tool does not require specialized hardware. The tool operates on a standard machine running Linux or Windows and is accessed via a command-line interface, such as Command Prompt (Windows) or Terminal (Linux).

**Network Interface Card (NIC):**
- Enables communication between the host machine and external cloud-based web servers over the internet
- Handles transmission and reception of IP packets
- Supports TCP/IP networking stack
- Capable of handling encrypted traffic (TLS/SSL) at the hardware level

Overall, this tool requires only standard computing hardware. The primary hardware dependency is the network interface used to communicate with remote cloud-based web servers.

### 3.2 Software Interfaces

The external software interfaces for this product are as follows:

| Interface | Details |
|---|---|
| **Database** | SQLite database for storing diagnostic results for cloud servers |
| **Operating System** | Windows 10/11 and Linux (Ubuntu 22.04 LTS or later). Provides: network stack (TCP/IP), system clock (for timestamp generation), and file system access (for report and archive creation) |
| **Web Server Communication** | Communicates with cloud-hosted web servers (Google Cloud, Amazon EC2, Microsoft Azure) using HTTP/1.1 or HTTP/2, HTTPS over TLS 1.2+. Used to determine server availability, measure RTT, and validate SSL certificate expiration |
| **Email Service** | Integrates with SMTP-compatible email services (Gmail SMTP, Outlook SMTP). Outgoing data includes: email notification, encrypted password-protected archive file attachment, error code, description, timestamp, and performance metrics (average and median RTT) |

**Shared Internal Data:**
- Monitoring results (status code, RTT values)
- Calculated average and median RTT
- SSL expiration status
- Timestamp of detection

Data sharing occurs through structured objects or configuration files within the application. No global shared memory mechanism is required.

**Communication Protocols:**
- All communications are over TCP/IP
- Stateless HTTP requests for monitoring
- Encrypted email transmission via SMTP over TLS

### 3.3 Communications Interfaces

All communication occurs over TCP/IP and standard networking protocols:

- **HTTP/HTTPS:** Stateless requests to communicate with the web server over a WAN connection
- **RTT Sampling:** 100 requests of payload per monitoring cycle
- **SMTP:** Email communication to the server owner with encrypted attachments
- **Notification Timing:** Notifications sent within 24 hours of problem detection

---

## 4. System Features

### 4.1 Web Server Availability Monitoring

**REQ-1: `Web_Monitoring`**

#### 4.1.1 Description and Priority

The system periodically checks whether a specified web server URL is accessible. **Priority: High.**

#### 4.1.2 Stimulus/Response Sequences

| Step | Action |
|---|---|
| **Stimulus** | The system monitors whether a specified cloud-based web server is accessible. |
| **Response 1** | The system retrieves the configured target URL. If the target URL is invalid, the system returns "Invalid URL" and prompts for a different one. |
| **Response 2** | The system sends an HTTP/HTTPS request to the target server. |
| **Response 3** | The system waits for a server response within a defined timeout period. |
| **If valid response received** | The system records the HTTP status code, timestamp, and stores the result in the SQLite database. |
| **If no response received** | The system records a timeout failure and increases the monitoring interval to confirm the failure. |
| **If error persists** | The system logs the failure and marks the server status as "Down." |

#### 4.1.3 Functional Requirements

- The system shall send HTTP/HTTPS requests to the target URL.
- The system shall detect HTTP error codes.
- The system shall detect connection timeouts.
- The system shall log the timestamp of each check.
- The system shall store results in the local SQLite database.

---

### 4.2 Round-Trip Time Measurement

**REQ-2: `RTT_Measurement`**

#### 4.2.1 Description and Priority

The system measures network performance by calculating average and median RTT. **Priority: Medium.**

#### 4.2.2 Stimulus/Response Sequences

| Step | Action |
|---|---|
| **Stimulus** | The system measures the network latency between the host machine and the cloud server. |
| **Response 1** | The user sets the URL for the web server and starts the system. |
| **Response 2** | The system pings the server and receives HTTP GET responses. |
| **Response 3** | The system calculates average RTT and median RTT based on the time between pings. |

#### 4.2.3 Functional Requirements

- The system shall send at least 100 separate requests per monitoring cycle.
- The system shall calculate the average RTT.
- The system shall calculate the median RTT.
- The system shall store RTT statistics in the database.
- The system shall include RTT results in monitoring reports.

---

### 4.3 SSL Certificate Expiration Monitoring

**REQ-3: `SSL_Cert`**

#### 4.3.1 Description and Priority

The system checks whether the SSL certificate of the monitored web server is valid and not expired. **Priority: High.**

#### 4.3.2 Stimulus/Response Sequences

| Step | Action |
|---|---|
| **Stimulus** | The system verifies that the server's SSL certificate is valid and not expired. |
| **Response 1** | The system retrieves the SSL certificate during the TLS handshake. |
| **Response 2** | The system extracts the expiration date of the certificate. |
| **Response 3** | The system compares the current date and expiration date. |
| **If expired** | The system logs an SSL expiration error and flags the server as having a certificate issue. |

#### 4.3.3 Functional Requirements

- The system shall retrieve the SSL certificate from the server.
- The system shall extract the certificate's expiration date.
- The system shall determine whether the certificate is expired.
- The system shall log SSL status in the database.
- The system shall generate a warning if expiration is detected.

---

### 4.4 Error Detection and Classification

**REQ-4: `Error_Detect`**

#### 4.4.1 Description and Priority

The system identifies and categorizes detected failures. **Priority: High.**

#### 4.4.2 Stimulus/Response Sequences

| Step | Action |
|---|---|
| **Stimulus** | The system detects and categorizes server failures. |
| **Response 1** | The system identifies the type of failure. |
| **Response 2** | The system generates a brief description of the error. |
| **Response 3** | The system records the error code, description, and timestamps the detection event. |
| **Response 4** | The system stores the failure record in the database. |

#### 4.4.3 Functional Requirements

- The system shall classify HTTP error codes.
- The system shall detect DNS resolution failures.
- The system shall store error type and description.
- The system shall timestamp all detected failures.

---

### 4.5 Email Notification System

**REQ-5: `Email_Notif`**

#### 4.5.1 Description and Priority

The system notifies the server owner if an issue is detected. **Priority: High.**

#### 4.5.2 Stimulus/Response Sequences

| Step | Action |
|---|---|
| **Stimulus** | The system notifies the server owner of detected issues. |
| **Response 1** | The system prepares an email message to the recipient. |
| **Response 2** | The system attaches the encrypted archive file. |
| **Response 3** | The system logs confirmation of email transmission. |
| **Response 4** | The system ensures the notification is sent within 24 hours of detection. |

#### 4.5.3 Functional Requirements

- The system shall generate a monitoring report upon failure detection.
- The system shall create an encrypted archive file.
- The system shall send notification within 24 hours of detection.
- The system shall include:
  - Error code
  - Description
  - Date and time detected

---

### 4.6 Encrypted Report Generation

**REQ-6: `Encrypt_Report`**

#### 4.6.1 Description and Priority

The system creates a secure diagnostics report for the server owner. **Priority: High.**

#### 4.6.2 Stimulus/Response Sequences

| Step | Action |
|---|---|
| **Stimulus** | The system generates a secure diagnostic report when a failure is detected. |
| **Response 1** | The system compiles monitoring data including error code, error description, date/time detected, and RTT statistics. |
| **Response 2** | The system generates a structured report file. |
| **Response 3** | The system compresses the archive file. |
| **Response 4** | The system encrypts the archive file using AES-256. |
| **Response 5** | The system stores the encrypted archive locally. |

#### 4.6.3 Functional Requirements

- The system shall generate a structured report file.
- The system shall compress the report file.
- The system shall encrypt the archive using AES-256.
- The system shall store a copy locally.

---

### 4.7 Persistent Data Storage (SQLite Database)

**REQ-7: `Data_Store`**

#### 4.7.1 Description and Priority

The system stores monitoring results and detection history. **Priority: High.**

#### 4.7.2 Stimulus/Response Sequences

| Step | Action |
|---|---|
| **Stimulus** | The system maintains historical monitoring records. |
| **Response 1** | The system creates a new database entry. |
| **Response 2** | The system stores timestamp, server URL, availability status, HTTP status code, RTT statistics, and SSL status. |

#### 4.7.3 Functional Requirements

- The system shall store each monitored event.
- The system shall store timestamps.
- The system shall store RTT statistics.
- The system shall store SSL status.
- The system shall allow retrieval of historical monitoring data.

---

### 4.8 Scheduled Monitoring Execution

**REQ-8: `Sched_Monitor`**

#### 4.8.1 Description and Priority

The system automatically performs monitoring at predefined intervals. **Priority: High.**

#### 4.8.2 Stimulus/Response Sequences

| Step | Action |
|---|---|
| **Stimulus** | The system timer reaches the configured monitoring interval. |
| **Response 1** | The system initiates a new monitoring cycle. |
| **Response 2** | The system performs availability checks. |
| **Response 3** | The system performs RTT measurements. |
| **Response 4** | The system performs SSL validation. |
| **Response 5** | The system logs the results and resets the timer for the next cycle. |

#### 4.8.3 Functional Requirements

- The system shall support configurable monitoring intervals.
- The system shall run continuously in the background.
- The system shall log each execution cycle.
- The system shall increase intervals if there are repeated error codes to ensure accuracy.

---

## 5. Other Nonfunctional Requirements

### 5.1 Performance Requirements

| ID | Requirement | Target |
|---|---|---|
| **PERF-1** | RTT measurement completion | The system shall complete 100 RTT measurements within **120 seconds** per server under normal network conditions. |
| **PERF-2** | Notification dispatch | The system shall send notifications within **24 hours** of detecting a failure or SSL expiration. |
| **PERF-3** | RTT calculation accuracy | RTT calculations shall be accurate within **1 millisecond** of the measured value. |
| **PERF-4** | Minimum monitoring capacity | The system shall support monitoring at least **one website** on a standard host machine. |
| **PERF-5** | Database write latency | A single monitoring result (including all 100 RTT samples) shall be written to the SQLite database within **500 milliseconds**. |
| **PERF-6** | Database read latency | Retrieving the most recent 50 monitoring runs for a target shall complete within **200 milliseconds**. |
| **PERF-7** | Email delivery time | Once an email notification has been sent via SMTP, it shall be delivered to the recipient's mail server within **5 minutes** under normal network conditions. Delivery to the recipient's inbox depends on the external mail provider but is expected within **15 minutes** in typical scenarios. |
| **PERF-8** | Report generation time | The system shall generate, compress, and encrypt a diagnostic report within **10 seconds** of initiating the report generation process. |
| **PERF-9** | Availability check response | An individual HTTP availability check (single request) shall complete or time out within **30 seconds**. |
| **PERF-10** | SSL certificate retrieval | SSL certificate retrieval and validation shall complete within **10 seconds** per server. |
| **PERF-11** | System startup time | The system shall be fully initialized and ready to begin monitoring within **5 seconds** of launch on a standard host machine. |
| **PERF-12** | End-to-end notification latency | The total elapsed time from failure detection to the notification email being dispatched via SMTP shall not exceed **2 minutes** (excluding retry delays). This includes report generation, encryption, and email transmission. |

### 5.2 Safety Requirements

Not Applicable.

### 5.3 Security Requirements

| ID | Requirement |
|---|---|
| **SEC-1** | **TLS Protocol Standard** — All HTTP monitoring over HTTPS shall use TLS 1.2 or higher. |
| **SEC-2** | **Email Transmission Security** — All email communications shall use SMTP over TLS (STARTTLS). This ensures that the connection between the monitoring tool and email service provider is fully encrypted. |
| **SEC-3** | **Diagnostic Report Encryption** — Diagnostic reports shall be encrypted using AES-256 encryption. Reports must be bundled into a password-protected archive before being sent as an attachment. |
| **SEC-4** | **Out-of-Band Password Management** — Archive passwords shall not be transmitted in plaintext within the same email body. Passwords must be managed via secure environment variables or pre-shared keys. |
| **SEC-5** | **Credentials Storage Security** — SMTP credentials shall not be stored in plaintext. They must be stored in a protected configuration file or environment variables with restricted access. |
| **SEC-6** | **Database File Security** — The SQLite database file shall be protected by operating system access controls. |

### 5.4 Software Quality Attributes

#### 5.4.1 Maintainability

- The source code shall use modular design principles to improve maintainability and testability. The system will separate monitoring, database access, report generation, and email delivery into distinct modules.
- The source code shall use good commenting standards, adding comments wherever meaningful. Each function shall have at least one comment describing purpose and input/output.

#### 5.4.2 Portability

- The system shall function via Python 3 and use standard libraries.
- The system shall not be affected by the web server provider.

#### 5.4.3 Reliability

- The system shall perform monitoring tasks at regular intervals without interruption (configurable: e.g., every 30 minutes or every hour).
- The system shall be capable of handling web servers that are down without crashing.
- Email notifications shall be sent within 24 hours of detection of disruptions.
- All interactions with web servers shall be recorded in the SQLite database.

#### 5.4.4 Usability

- The system shall include error descriptions in reports whenever possible, as well as time and date of the disruption.
- New web servers shall be able to be added to the monitoring list with fewer than 10 commands.
- The `README.md` will outline all major interactions and usage instructions.

---

## 6. Other Requirements

No other requirements.

---

## 7. Analysis Models

This chart displays a use case diagram of the web server monitoring system. The users (entities) include the web server, developer, IT analyst, and server owner/admin. Their interactions with the system are shown visually.

![Use Case Diagram](diagrams/use_case_diagram.png)

---

## Appendix A: Glossary

| Term | Definition |
|---|---|
| **SRS** | Software Requirements Specification |
| **SDS** | Software Design Specification |
| **Packet** | Small, formatted unit of data sent over a network |
| **WAN** | Wide-Area Network — a large-scale telecommunications network, such as the Internet, connecting smaller networks |
| **RTT** | Round-Trip Time — time measured in milliseconds (ms) for a data packet to travel from a source to a destination and for the response to return |
| **HTTP** | Hypertext Transfer Protocol — foundational application-layer protocol for data communication on the World Wide Web |
| **TCP/IP** | Transmission Control Protocol/Internet Protocol — fundamental communication protocols used to interconnect network devices on the Internet |
| **SSL** | Secure Sockets Layer — networking security protocol that encrypts data transmitted between a web server and a browser, ensuring privacy, data integrity, and authentication |
| **TLS** | Transport Layer Security — successor to SSL; provides encryption and data integrity |
| **SMTP** | Simple Mail Transfer Protocol — standard application-layer protocol for sending and relaying email across the Internet |
| **SQLite** | Lightweight, serverless, embedded relational database engine |
| **AES-256** | Advanced Encryption Standard with 256-bit key — industry-standard encryption algorithm |
| **HTTPS** | HTTP Secure — HTTP over TLS for encrypted communication |
| **CLI** | Command-Line Interface — text-based interface for interacting with an application |
