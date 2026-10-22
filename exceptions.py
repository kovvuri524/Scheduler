"""
Custom Exceptions

Purpose:
--------
Contains application-specific exceptions
used by the scheduler application.

Exceptions:
-----------
DuplicateScanError
------------------
Raised when a scan has already been
processed and its name exists in
processed_scans.txt.

Usage:
------
Used by:
    - start_handler.py
    - scheduler.py

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
       SMTP failure.
       Unexpected runtime error.

Behavior:
---------
DuplicateScanError:
    - No retries.
    - Duplicate notification email sent.

Technical Errors:
    - Retry up to 3 times.
    - Failure notification email sent
      after all retries are exhausted.
"""

class DuplicateScanError(Exception):
    """
    Raised when a scan has already
    been processed.
    """
    pass
