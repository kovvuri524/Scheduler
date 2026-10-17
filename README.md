# Scheduler Project

This project reads scan schedule information from a CSV file and prints start and end messages when the configured times are reached.

## Sample CSV Format

| Scan_name | Start_time | End_time |
|-----------|------------|----------|
| ScanA | 20261017 150000 | 20261017 151000 |
| ScanB | 20261017 153000 | 20261017 154000 |

## Project Structure

Project/
│
├── scheduler.py
├── sample_scans.csv
├── README.md
├── requirements.txt
└── .gitignore

## Before running the program

1. Copy sample_scans.csv to scans.csv
2. Update the schedule values in scans.csv
3. Run the program

## Windows Setup

Create Virtual Environment

python -m venv venv

Activate Virtual Environment

.\venv\Scripts\Activate.ps1

Install Dependencies

pip install -r requirements.txt

Run the Program

python scheduler.py

## Linux / macOS Setup

Create Virtual Environment

python3 -m venv venv

Activate Virtual Environment

source venv/bin/activate

Install Dependencies

pip install -r requirements.txt

Run the Program

python3 scheduler.py


