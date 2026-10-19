"""
Custom Exceptions

Purpose:
--------
Contains application-specific exceptions
used by the scheduler.

Exceptions:
-----------

DuplicateScanError
------------------
Raised when a scan has already been processed
and a corresponding JSON file already exists.

Usage:
------
Used by:
    - start_handler.py
    - end_handler.py

Purpose:
--------
Allows the scheduler to distinguish between:

1. Business Validation Errors
   Example:
       Scan already processed.

2. Technical Errors
   Example:
       File access issue.
       Permission issue.
       Unexpected runtime error.

Behavior:
---------
DuplicateScanError:
    - Prints FAILED.
    - No retries.

Technical Errors:
    - Retry 3 times.
"""

class DuplicateScanError(Exception):
    pass