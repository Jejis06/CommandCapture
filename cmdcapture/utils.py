"""
Utility functions for the Command Capture library.
"""

import shutil
import subprocess
from typing import Optional


def which(command: str) -> Optional[str]:
    """
    Find the full path to a command, similar to the 'which' command.
    
    Args:
        command: The command to find
        
    Returns:
        The full path to the command if found, None otherwise
    """
    return shutil.which(command)


def is_command_available(command: str) -> bool:
    """
    Check if a command is available in the system PATH.
    
    Args:
        command: The command to check
        
    Returns:
        True if command is available, False otherwise
    """
    return which(command) is not None


def split_command(command: str) -> list:
    """
    Split a command string into a list of arguments.
    Handles quoted arguments properly.
    
    Args:
        command: The command string to split
        
    Returns:
        List of command arguments
    """
    import shlex
    return shlex.split(command) 