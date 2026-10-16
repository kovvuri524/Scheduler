CSV-Based Scan Scheduler

Overview

A Python-based scheduler that reads scan names, start times, and end times from a CSV file and prints messages at the scheduled times. 
Project Structure

project/
├── scans.csv
├── scan_scheduler.py
└── README.md

CSV Format

scan_name,start_time,end_time
Scan_A,20261016 220500,20261016 221000
Scan_B,20261016 221100,20261016 222000
Time format: HH:MM (24-hour format).

Requirements

Python 3.x

How to Run

Windows

python scan_scheduler.py

Mac/Linux

python3 scheduler.py
