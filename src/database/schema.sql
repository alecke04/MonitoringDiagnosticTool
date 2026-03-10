-- schema.sql
-- SQLite database schema for the Monitoring and Diagnostics Tool
-- Executed once on first run to initialize all tables
-- See SDS Section 5 for full table definitions and constraints

-- Table 1: monitored_targets
-- Stores configuration for each web server being monitored
CREATE TABLE IF NOT EXISTS monitored_targets (
    target_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    url             TEXT    NOT NULL UNIQUE,        -- server URL (alternate key)
    sample_path     TEXT    NOT NULL,               -- path to 1KB synthetic payload
    email_recipient TEXT    NOT NULL,               -- alert destination email
    interval        INTEGER NOT NULL,               -- monitoring interval in seconds
    timeout         INTEGER NOT NULL,               -- request timeout in seconds
    retry_count     INTEGER NOT NULL                -- retries before marking down
);

-- Table 2: monitored_runs
-- Stores the result of each monitoring cycle for each target
CREATE TABLE IF NOT EXISTS monitored_runs (
    run_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    target_id       INTEGER NOT NULL,
    timestamp       TEXT    NOT NULL,               -- ISO 8601 datetime with timezone
    reachable       INTEGER NOT NULL,               -- 0 = down, 1 = up (SQLite bool)
    http_status     INTEGER,                        -- HTTP response code
    error_code      TEXT,                           -- standardized error label
    ssl_expiration  TEXT,                           -- cert expiry date or status
    avg_rtt         REAL    CHECK(avg_rtt >= 0),    -- average RTT in ms
    median_rtt      REAL    CHECK(median_rtt >= 0), -- median RTT in ms
    FOREIGN KEY (target_id) REFERENCES monitored_targets(target_id)
);

-- Table 3: rtt_samples
-- Stores all 100 individual RTT measurements per monitoring run
CREATE TABLE IF NOT EXISTS rtt_samples (
    sample_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          INTEGER NOT NULL,
    rtt_value       REAL    NOT NULL CHECK(rtt_value >= 0),  -- single RTT in ms
    FOREIGN KEY (run_id) REFERENCES monitored_runs(run_id)
);

-- Table 4: notifications
-- Logs each email notification event tied to a monitoring run
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          INTEGER NOT NULL,
    sent_status     TEXT    CHECK(sent_status IN ('PENDING', 'SENT', 'FAILED')),
    filename        TEXT,                           -- encrypted ZIP archive filename
    time_sent       TEXT,                           -- ISO 8601 timestamp of send
    FOREIGN KEY (run_id) REFERENCES monitored_runs(run_id)
);
