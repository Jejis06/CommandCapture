"""
Command Capture Library

A Python library for capturing output from terminal commands with advanced features.
"""

from .core import CommandCapture, CaptureResult
from .exceptions import CommandError, TimeoutError
from .utils import which, is_command_available

__version__ = "1.0.0"
__author__ = "Command Capture Library"
__all__ = [
    "CommandCapture",
    "CaptureResult", 
    "CommandError",
    "TimeoutError",
    "which",
    "is_command_available"
] 