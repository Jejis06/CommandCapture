"""
Custom exceptions for the Command Capture library.
"""


class CommandError(Exception):
    """Raised when a command execution fails."""
    
    def __init__(self, message, return_code=None, command=None):
        super().__init__(message)
        self.return_code = return_code
        self.command = command


class TimeoutError(Exception):
    """Raised when a command execution times out."""
    
    def __init__(self, message, timeout=None, command=None):
        super().__init__(message)
        self.timeout = timeout
        self.command = command 