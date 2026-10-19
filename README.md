# Scheduler Project

## Overview

This project reads scan schedule information from a CSV file and creates JSON files when the configured start and end times are reached.

The scheduler:

- Reads scan schedules from `scans.csv`
- Triggers start and end events 1 minute after the configured times
- Creates JSON files for start and end events
- Stores JSON files in dedicated folders
- Supports retry logic for technical failures
- Prevents duplicate scan processing
- Supports Windows, Linux, and macOS

## Features

### Start Event

When the configured start time is reached:

- Creates a JSON file in the `start_time` folder
- Generates a timestamped filename
- Validates whether the scan has already been processed

Example:

```text
start_time/
└── ScanA_start_duration20261019150000.json
```

### End Event

When the configured end time is reached:

- Creates a JSON file in the `end_time` folder
- Generates a timestamped filename
- Validates whether the scan has already been processed

Example:

```text
end_time/
└── ScanA_end_duration20261019151000.json
```

## Duplicate File Validation

Before creating a JSON file, the handler checks whether a file already exists for the same scan.

Example:

```text
ScanA_start_duration20261019150000.json
```

If a matching file already exists:

```text
FAILED
```

is displayed and no new file is created.

## Retry Logic

Technical failures are automatically retried.

Examples:

- Permission issues
- File system errors
- Missing folders
- Temporary operating system failures

Retry behavior:

- Maximum Retries: 3
- Retry Wait Time: Random value between 15 and 25 seconds

Example:

```text
Retry 1
↓
Wait 20 seconds

Retry 2
↓
Wait 18 seconds

Retry 3
↓
Failed
```

Duplicate records are not retried.

## Sample CSV Format

| Scan_name | Start_time | End_time |
|------------|------------|------------|
| ScanA | 20261019150000 | 20261019151000 |
| ScanB | 20261019153000 | 20261019154000 |

### Time Format

```text
YYYYMMDDHHMMSS
```

Example:

```text
20261019153045
```

## Generated JSON Format

### Start Event

**File**

```text
ScanA_start_duration20261019150000.json
```

**Content**

```json
{
    "scan_name": "ScanA",
    "time": "20261019150000"
}
```

### End Event

**File**

```text
ScanA_end_duration20261019151000.json
```

**Content**

```json
{
    "scan_name": "ScanA",
    "time": "20261019151000"
}
```

## Project Structure

```text
Project/
│
├── scheduler.py
├── scans.csv
├── exceptions.py
├── README.md
├── requirements.txt
│
├── handlers/
│   ├── start_handler.py
│   └── end_handler.py
│
├── start_time/
│
└── end_time/
```

## Components

### scheduler.py

Main scheduler process.

Responsibilities:

- Read CSV schedule data
- Monitor start and end times
- Execute retry logic
- Trigger start and end handlers
- Track job completion

### handlers/start_handler.py

Responsible for:

- Start event processing
- Duplicate validation
- Start JSON creation

### handlers/end_handler.py

Responsible for:

- End event processing
- Duplicate validation
- End JSON creation

### exceptions.py
Contains custom application exceptions.
Current exception:
DuplicateScanError
Used when a scan has already been processed.

# Windows Setup
## Create Virtual Environment

python -m venv .venv

## Activate Virtual Environment

.\.venv\Scripts\Activate.ps1

## Install Dependencies

pip install -r requirements.txt

## Run Scheduler

python scheduler.py

# Linux / macOS Setup

## Create Virtual Environment

python3 -m venv .venv

## Activate Virtual Environment

source .venv/bin/activate

## Install Dependencies

pip install -r requirements.txt

## Run Scheduler

python3 scheduler.py

# Supported Platforms
Windows
Linux
macOS
