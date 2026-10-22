# Scheduler Project

## Overview

This project reads scan schedule information from a CSV file and sends email notifications when configured start and end times are reached.

The scheduler:

- Reads scan schedules from `scans.csv`
- Triggers start events 1 minute after the configured start time
- Triggers end events 2 minutes after the configured end time
- Sends email notifications for scan start and completion
- Sends failure notifications after retry exhaustion
- Prevents duplicate scan processing
- Supports retry logic for technical failures
- Supports Windows, Linux, and macOS

---

# Features

## Start Event

When the configured start time is reached:

- Validates whether the scan has already been processed
- Sends a Start Notification email
- Stores the scan name in `processed_scans.txt`

### Example

**Subject**

```text
Scan Started - ScanA
```

**Body**

```text
Hello,

The scan "ScanA" has started successfully.

Start Time:
20261022153000

Regards,
Scheduler Application
```

---

## End Event

When the configured end time is reached:

- Sends a Completion Notification email

### Example

**Subject**

```text
Scan Completed - ScanA
```

**Body**

```text
Hello,

The scan "ScanA" has completed successfully.

End Time:
20261022154000

Regards,
Scheduler Application
```

---

## Duplicate Scan Validation

Before processing a scan, the application checks whether the scan name already exists in:

```text
processed_scans.txt
```

### Example

```text
ScanA
ScanB
ScanC
```

If the scan already exists:

```text
ScanA already processed
```

A duplicate notification email is sent.

### Example

**Subject**

```text
Duplicate Scan - ScanA
```

**Body**

```text
Hello,

The scan "ScanA" has already been processed.

No further action was taken.

Regards,
Scheduler Application
```

---

## Retry Logic

Technical failures are automatically retried.

### Examples

- File system errors
- Permission issues
- SMTP connection failures
- Unexpected runtime errors

### Retry Behavior

```text
Maximum Retries : 3
Retry Wait Time : 15–25 Seconds
```

### Example

```text
Retry 1
↓
Wait 20 seconds

Retry 2
↓
Wait 18 seconds

Retry 3
↓
FAILED
```

Duplicate scans are not retried.

---

## Failure Notifications

If all retry attempts fail, the scheduler sends a failure email.

### Example

**Subject**

```text
Scan Failed - ScanA
```

**Body**

```text
Hello,

The scan "ScanA" could not be processed.

Reason:
FileNotFoundError

Retry Attempts:
3

Failure Time:
20261022154500

Regards,
Scheduler Application
```

---

# Sample CSV Format

```csv
Scan_name,Start_time,End_time
ScanA,20261022150000,20261022151000
ScanB,20261022153000,20261022154000
```

---

## Time Format

```text
YYYYMMDDHHMMSS
```

### Example

```text
20261022153045
```

---

# Email Notifications

## Start Notification

```text
Scan Started - ScanA
```

## Completion Notification

```text
Scan Completed - ScanA
```

## Duplicate Notification

```text
Duplicate Scan - ScanA
```

## Failure Notification

```text
Scan Failed - ScanA
```

---

# Project Structure

```text
project/
│
├── scheduler.py
├── exceptions.py
├── scans.csv
├── processed_scans.txt
├── requirements.txt
├── Dockerfile
├── .env
├── README.md
│
├── handlers/
│   ├── __init__.py
│   ├── email_handler.py
│   ├── start_handler.py
│   └── end_handler.py
│
└── .gitignore
```

---

# Components

## scheduler.py

Main scheduler process.

### Responsibilities

- Read scan schedules from CSV
- Monitor configured start and end times
- Execute retry logic
- Handle duplicate scans
- Trigger start and end handlers
- Send duplicate and failure notifications
- Track job completion

---

## handlers/start_handler.py

Responsible for:

- Start event processing
- Duplicate scan validation
- Start notification emails
- Updating `processed_scans.txt`

---

## handlers/end_handler.py

Responsible for:

- End event processing
- Completion notification emails

---

## handlers/email_handler.py

Responsible for:

- SMTP connection management
- Gmail authentication
- Email creation
- Email delivery
- Notification handling

---

## exceptions.py

Contains custom application exceptions.

### Current Exception

```python
DuplicateScanError
```

Raised when a scan has already been processed.

---

# Environment Variables

Create a `.env` file:

```env
EMAIL_ID=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
RECIPIENT_EMAIL=recipient@gmail.com
```

---

# Windows Setup

## Create Virtual Environment

```powershell
python -m venv .venv
```

## Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

## Install Dependencies

```powershell
pip install -r requirements.txt
```

## Run Scheduler

```powershell
python scheduler.py
```

---

# Linux / macOS Setup

## Create Virtual Environment

```bash
python3 -m venv .venv
```

## Activate Virtual Environment

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Scheduler

```bash
python3 scheduler.py
```

# Supported Platforms

- Windows
- Linux
- macOS


