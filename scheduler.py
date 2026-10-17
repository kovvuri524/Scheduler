"""
Scheduler Program

This script reads scan schedules from a CSV file
and prints start and end messages at configured times.

The start event runs 1 minute after Start_time.
The end event runs 1 minute after End_time.

Supported Platforms:
- Windows
- Linux
- macOS
"""

import csv
import time
from datetime import datetime, timedelta

jobs = []

# Read runtime CSV file
with open("scans.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        jobs.append({
            "scan_name": row["Scan_name"],
            "start_time": datetime.strptime(
                row["Start_time"],
                "%Y%m%d %H%M%S"
            ) + timedelta(minutes=1),
            "end_time": datetime.strptime(
                row["End_time"],
                "%Y%m%d %H%M%S"
            ) + timedelta(minutes=1),
            "start_done": False,
            "end_done": False
        })

print("Monitoring started...")

while True:
    current_time = datetime.now()

    for job in jobs:

        if not job["start_done"] and current_time >= job["start_time"]:
            print(
                f"Started cronjob for {job['scan_name']} "
                f"at {current_time.strftime('%Y%m%d %H%M%S')}"
            )
            job["start_done"] = True

        if not job["end_done"] and current_time >= job["end_time"]:
            print(
                f"Ended cronjob for {job['scan_name']} "
                f"at {current_time.strftime('%Y%m%d %H%M%S')}"
            )
            job["end_done"] = True

    if all(job["start_done"] and job["end_done"] for job in jobs):
        print("All jobs completed.")
        break

    time.sleep(1)
