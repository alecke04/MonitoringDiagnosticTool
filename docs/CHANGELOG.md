# Changelog — SDS & SRS Revisions

**Date:** March 8, 2026  
**Author:** Alec Brenes  

---

## Overview

This document logs all changes made to the Software Design Specification (SDS) and Software Requirements Specification (SRS) based on professor feedback (Ilya Tsoy, Mar 5 at 5:18 PM).

---

## Professor Feedback Addressed

| Issue | Points | Resolution |
|---|---|---|
| Table of contents page numbers do not reflect actual section pages | -2 | Replaced page numbers with Markdown anchor links that always resolve correctly |
| Chapter 5.1: Add more performance requirements (e.g., DB read/write time, notification delivery time) | -2 | Expanded from 4 to 12 performance requirements with specific targets |

---

## Changes to SDS.md

### Formatting & Presentation
- Converted entire document from plain text to properly formatted Markdown
- Added Markdown table of contents with anchor links (no page numbers — resolves correctly in rendered Markdown)
- Organized all sections with consistent heading hierarchy (`#`, `##`, `###`, `####`)
- Replaced inline lists with formatted Markdown tables throughout


### Completed Missing Sections
- **Section 4.3 — Sequence Diagram:** Added two full sequence diagrams:
  - Scenario 1: Successful Monitoring Cycle (No Errors)
  - Scenario 2: Server Down — Failure Notification Flow

### Database Design Fixes
- Reformatted all table definitions into proper column/type/constraint tables
- Added SQL-style constraint syntax (e.g., `CHECK(rtt_value >= 0)`)

### Class Diagram Documentation
- Documented all 9 classes with attribute/method tables
- Added class relationships table with cardinality

### User Interface Design
- Added CLI command table with example terminal output

### Typo Fixes
- "indiccator" → "indicator"
- "reachabilit" → "reachability"
- "msut" → "must"
- "Constrains" → "Constraints"

---

## Changes to SRS.md

### Formatting & Presentation
- Converted entire document from plain text to properly formatted Markdown
- Added Markdown table of contents with anchor links
- Organized sections with consistent heading hierarchy
- Replaced inline lists with formatted Markdown tables

### Section 5.1 — Performance Requirements (Professor Feedback)
Expanded from 4 requirements to 12. New requirements added:

| ID | New Requirement | Target |
|---|---|---|
| PERF-5 | Database write latency (single monitoring result + 100 RTT samples) | ≤ 500 ms |
| PERF-6 | Database read latency (50 most recent runs) | ≤ 200 ms |
| PERF-7 | Email delivery time (SMTP to recipient mail server) | ≤ 5 min; inbox delivery ≤ 15 min |
| PERF-8 | Report generation, compression, and encryption | ≤ 10 seconds |
| PERF-9 | Individual HTTP availability check timeout | ≤ 30 seconds |
| PERF-10 | SSL certificate retrieval and validation | ≤ 10 seconds |
| PERF-11 | System startup and initialization | ≤ 5 seconds |
| PERF-12 | End-to-end notification latency (detection → SMTP dispatch, excluding retries) | ≤ 2 minutes |

### Section Numbering Fix
- Fixed duplicate `4.1.1` / `4.1.2` / `4.1.3` numbering across all system features
- Each feature now uses unique numbering: `4.1.x`, `4.2.x`, `4.3.x`, etc.

### Other Improvements
- Security requirements formatted into a numbered table (SEC-1 through SEC-6)
- Software quality attributes organized with clear sub-headers
- Glossary formatted as a proper Markdown table

---

## New Files Created

| File | Purpose |
|---|---|
| `README.md` | Project overview, folder structure, installation/usage instructions, architecture summary |
| `CHANGELOG.md` | This document — tracks all revisions made |

---

## Repository Structure

Created the expected project folder structure as defined in the README. See `README.md` for the full directory tree.
