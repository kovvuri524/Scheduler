CSV-Based Scan Scheduler

Overview

A Python-based scheduler that reads scan names, start times, and end times from a CSV file and prints messages at the scheduled times. 
Project Structure

scan-scheduler/
├── scans.csv
├── scan_scheduler.py
└── README.md

CSV Format

scan_name,start_time,end_time
Scan_A,10:00,17:00
Scan_B,11:00,18:00

Time format: HH:MM (24-hour format).

Requirements

Python 3.x

How to Run

Windows

python scan_scheduler.py
