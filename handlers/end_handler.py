"""
End Handler

Purpose:
--------
Creates an end JSON file when a scheduled
scan end event is triggered.

Responsibilities:
-----------------
1. Validate whether an end JSON already exists.
2. Prevent duplicate end processing.
3. Generate timestamp.
4. Create JSON file in end_time folder.

Output Example:
---------------
File Name:
ScanA_end_duration20261019150600.json

JSON:
{
    "scan_name": "ScanA",
    "time": "20261019150600"
}

Exceptions:
-----------
DuplicateScanError
    Raised when an end JSON file for
    the scan already exists.
"""

import json
import os

from datetime import datetime
from exceptions import DuplicateScanError


async def process_end(scan_name):

    existing_files = [
        file
        for file in os.listdir("end_time")
        if file.startswith(
            f"{scan_name}_end_duration"
        )
    ]

    if existing_files:
        raise DuplicateScanError(
            f"{scan_name} already processed"
        )

    timestamp = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )

    file_name = (
        f"{scan_name}_end_duration"
        f"{timestamp}.json"
    )

    file_path = os.path.join(
        "end_time",
        file_name
    )

    data = {
        "scan_name": scan_name,
        "end_time": timestamp
    }

    with open(file_path, "w") as json_file:
        json.dump(
            data,
            json_file,
            indent=4
        )