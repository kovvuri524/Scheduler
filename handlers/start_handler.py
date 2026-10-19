"""
Start Handler

Purpose:
--------
Creates a start JSON file when a scheduled
scan start event is triggered.

Responsibilities:
-----------------
1. Validate whether a start JSON already exists.
2. Prevent duplicate start processing.
3. Generate timestamp.
4. Create JSON file in start_time folder.

Output Example:
---------------
File Name:
ScanA_start_duration20261019150100.json

JSON:
{
    "scan_name": "ScanA",
    "time": "20261019150100"
}

Exceptions:
-----------
DuplicateScanError
    Raised when a start JSON file for
    the scan already exists.
"""

import json
import os

from datetime import datetime
from exceptions import DuplicateScanError


async def process_start(scan_name):

    existing_files = [
        file
        for file in os.listdir("start_time")
        if file.startswith(
            f"{scan_name}_start_duration"
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
        f"{scan_name}_start_duration"
        f"{timestamp}.json"
    )

    file_path = os.path.join(
        "start_time",
        file_name
    )

    # file_path = os.path.join(
    # "wrong_folder",
    # file_name
    # )

    data = {
        "scan_name": scan_name,
        "start_time": timestamp
    }

    with open(file_path, "w") as json_file:
        json.dump(
            data,
            json_file,
            indent=4
        )

