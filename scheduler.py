"""
Scheduler Program

Purpose:
--------
Reads scan schedules from scans.csv and creates JSON files
when the configured start and end times are reached.

Features:
---------
1. Reads scan schedules from CSV.
2. Executes start events 1 minute after the configured times.Executes end events 2 minute after the configured times.
3. Calls dedicated handlers for start and end events.
4. Supports retry mechanism for technical failures.
5. Creates JSON files in start_time and end_time folders.
6. Prevents duplicate scan processing.
7. Works on Windows, Linux, and macOS.

CSV Format:
-----------
Scan_name,Start_time,End_time
ScanA,20261019150000,20261019150100

Time Format:
------------
YYYYMMDDHHMMSS

Example:
--------
20261019153045

Retry Logic:
------------
Technical Failures:
    - Retries 3 times.
    - Waits 15–25 seconds between retries.

Duplicate Files:
    - Marked as FAILED.
    - No retries performed.
"""


import csv
import os
import asyncio
import random

from datetime import datetime, timedelta

from handlers.start_handler import process_start
from handlers.end_handler import process_end
from exceptions import DuplicateScanError

jobs = []

os.makedirs(
    "start_time",
    exist_ok=True
)

os.makedirs(
    "end_time",
    exist_ok=True
)

try:

    with open("scans.csv", "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            jobs.append({

                "scan_name":
                    row["Scan_name"],

                "start_time":
                    datetime.strptime(
                        row["Start_time"],
                        "%Y%m%d%H%M%S"
                    ) + timedelta(minutes=1),

                "end_time":
                    datetime.strptime(
                        row["End_time"],
                        "%Y%m%d%H%M%S"
                    ) + timedelta(minutes=2),

                "start_done": False,
                "end_done": False
            })

except Exception:

    print("FAILED")
    exit()


async def execute_with_retry(
    function,
    scan_name
):

    for attempt in range(1, 4):

        try:

            await function(scan_name)

            return True

        except DuplicateScanError:

            print("FAILED")

            return True

        except Exception as e:

            if attempt < 3:

                wait_time = random.randint(
                    15,
                    25
                )

                print(
                    f"Technical error: {e}"
                )

                print(
                    f"Retry {attempt}/3 in {wait_time} seconds"
                )

                await asyncio.sleep(
                    wait_time
                )

            else:

                print(
                    f"Technical error: {e}"
                )

                print("FAILED")

                return False

    return False


async def monitor():

    while True:

        current_time = datetime.now()

        for job in jobs:

            if (
                not job["start_done"]
                and current_time >= job["start_time"]
            ):

                await execute_with_retry(
                    process_start,
                    job["scan_name"]
                )

                job["start_done"] = True

            if (
                not job["end_done"]
                and current_time >= job["end_time"]
            ):

                await execute_with_retry(
                    process_end,
                    job["scan_name"]
                )

                job["end_done"] = True

        if all(
            job["start_done"]
            and job["end_done"]
            for job in jobs
        ):
            break

        await asyncio.sleep(1)


asyncio.run(
    monitor()
)
