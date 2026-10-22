"""
Scheduler Program

Purpose:
--------
Reads scan schedules from scans.csv and
triggers start and end email notifications
when configured times are reached.

Features:
---------
1. Reads scan schedules from CSV.
2. Triggers scan start notifications.
3. Triggers scan completion notifications.
4. Supports retry mechanism for technical failures.
5. Sends failure notifications after retry exhaustion.
6. Prevents duplicate scan processing.
7. Supports asynchronous execution.
8. Compatible with Docker deployment.

Workflow:
---------
CSV File
    ↓
Load Scan Schedule
    ↓
Monitor Current Time
    ↓
Start Time Reached
    ↓
process_start()
    ↓
Start Email Sent

End Time Reached
    ↓
process_end()
    ↓
Completion Email Sent

Duplicate Scan
    ↓
DuplicateScanError
    ↓
Duplicate Email Sent

Technical Error
    ↓
Retry 3 Times
    ↓
Failure Email Sent
"""

import csv
import asyncio
import random

from datetime import datetime, timedelta

from handlers.start_handler import process_start
from handlers.end_handler import process_end
from handlers.email_handler import send_email

from exceptions import DuplicateScanError


# Stores all scan jobs loaded from CSV
jobs = []


# Load scan configuration
try:

    with open(
        "scans.csv",
        "r"
    ) as file:

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

except Exception as error:

    print(
        f"Failed to load CSV: {error}"
    )

    exit()


async def execute_with_retry(
    function,
    scan_name
):
    """
    Execute a function with retry support.

    Parameters:
    ----------
    function
        Function to execute
        (process_start or process_end)

    scan_name
        Name of the scan.

    Behavior:
    ---------
    1. Executes target function.
    2. Retries 3 times for technical errors.
    3. Sends duplicate notification email
       for DuplicateScanError.
    4. Sends failure email when all retries
       are exhausted.
    """

    for attempt in range(1, 4):

        try:

            await function(
                scan_name
            )

            return True

        except DuplicateScanError:

            print(
                f"{scan_name} already processed"
            )

            try:

                await send_email(
                    subject=(
                        f"Duplicate Scan - "
                        f"{scan_name}"
                    ),
                    body=f"""
Hello,

The scan "{scan_name}" has already been processed.

No further action was taken.

Regards,
Scheduler Application
"""
                )

                print(
                    "Duplicate email sent."
                )

            except Exception as email_error:

                print(
                    f"Duplicate email error: "
                    f"{email_error}"
                )

            return True

        except Exception as error:

            print(
                f"Technical error: {error}"
            )

            if attempt < 3:

                wait_time = random.randint(
                    15,
                    25
                )

                print(
                    f"Retry {attempt}/3 "
                    f"in {wait_time} seconds"
                )

                await asyncio.sleep(
                    wait_time
                )

            else:

                print(
                    "All retry attempts exhausted."
                )

                try:

                    await send_email(
                        subject=(
                            f"Scan Failed - "
                            f"{scan_name}"
                        ),
                        body=f"""
Hello,

The scan "{scan_name}" could not be processed.

Reason:
{error}

Retry Attempts:
3

Failure Time:
{datetime.now().strftime('%Y%m%d%H%M%S')}

Regards,
Scheduler Application
"""
                    )

                    print(
                        "Failure email sent."
                    )

                except Exception as email_error:

                    print(
                        f"Failure email error: "
                        f"{email_error}"
                    )

                return False

    return False


async def monitor():
    """
    Continuously monitors all configured jobs.

    Behavior:
    ---------
    1. Checks current time every second.
    2. Triggers start event when
       start_time is reached.
    3. Triggers end event when
       end_time is reached.
    4. Stops when all jobs are completed.
    """

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


# Application Entry Point
asyncio.run(
    monitor()
)
