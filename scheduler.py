import csv
import time
from datetime import datetime

jobs = []

with open("scans.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        jobs.append({
            "scan_name": row["Scan_name"],
            "start_time": datetime.strptime(
                row["Start_time"],
                "%Y%m%d %H%M%S"
            ),
            "end_time": datetime.strptime(
                row["End_time"],
                "%Y%m%d %H%M%S"
            ),
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
                f"at {job['start_time']}"
            )
            job["start_done"] = True

        if not job["end_done"] and current_time >= job["end_time"]:
            print(
                f"Ended cronjob for {job['scan_name']} "
                f"at {job['end_time']}"
            )
            job["end_done"] = True

    if all(j["start_done"] and j["end_done"] for j in jobs):
        print("All jobs completed.")
        break

    time.sleep(1)