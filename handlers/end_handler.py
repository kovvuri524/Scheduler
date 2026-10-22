"""
End Handler

Purpose:
--------
Sends a notification email when a scheduled
scan reaches its configured end time.

Responsibilities:
-----------------
1. Generate end event timestamp.
2. Create scan completion message.
3. Trigger email notification.

Used By:
--------
- scheduler.py
"""

from datetime import datetime

from handlers.email_handler import send_email


async def process_end(scan_name):

    timestamp = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )

    await send_email(
        subject=f"Scan Completed - {scan_name}",
        body=f"""
Hello,

The scan "{scan_name}" has completed successfully.

End Time:
{timestamp}

Regards,
Scheduler Application
"""
    )
