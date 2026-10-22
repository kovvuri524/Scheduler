"""
Start Handler

Purpose:
--------
Sends a notification email when a scheduled
scan reaches its configured start time.

Responsibilities:
-----------------
1. Validate duplicate scan names.
2. Generate start event timestamp.
3. Send scan start notification.
4. Store processed scan names to prevent
   duplicate processing.

Used By:
--------
- scheduler.py
"""

from datetime import datetime

from handlers.email_handler import send_email
from exceptions import DuplicateScanError


async def process_start(scan_name):

    try:

        with open(
            "processed_scans.txt",
            "r"
        ) as file:

            processed_names = (
                file.read().splitlines()
            )

    except FileNotFoundError:

        processed_names = []

    if scan_name in processed_names:

        raise DuplicateScanError(
            f"{scan_name} already processed"
        )

    timestamp = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )

    await send_email(
        subject=f"Scan Started - {scan_name}",
        body=f"""
Hello,

The scan "{scan_name}" has started successfully.

Start Time:
{timestamp}

Regards,
Scheduler Application
"""
    )

    with open(
        "processed_scans.txt",
        "a"
    ) as file:

        file.write(
            f"{scan_name}\n"
        )
