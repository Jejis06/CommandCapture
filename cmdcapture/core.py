"""
Core functionality for the Command Capture library.
"""

import subprocess
import threading
import time
from dataclasses import dataclass
from typing import Optional, Union, List, Dict, Any, Callable
from pathlib import Path

from .exceptions import CommandError, TimeoutError
from .utils import split_command, is_command_available


@dataclass
class CaptureResult:
    """
    Result object containing all information about a command execution.
    """
    command: str
    return_code: int
    stdout: str
    stderr: str
    execution_time: float
    success: bool
    pid: Optional[int] = None
    
    def __str__(self) -> str:
        return f"CaptureResult(command='{self.command}', return_code={self.return_code}, success={self.success})"
    
    def __repr__(self) -> str:
        return self.__str__()


class CommandCapture:
    """
    A class for capturing output from terminal commands with advanced features.
    """
    
    def __init__(self, default_timeout: Optional[float] = None, 
                 default_cwd: Optional[Union[str, Path]] = None,
                 default_env: Optional[Dict[str, str]] = None):
        """
        Initialize CommandCapture with default settings.
        
        Args:
            default_timeout: Default timeout for commands in seconds
            default_cwd: Default working directory for commands
            default_env: Default environment variables
        """
        self.default_timeout = default_timeout
        self.default_cwd = Path(default_cwd) if default_cwd else None
        self.default_env = default_env or {}
        
    def run(self, command: Union[str, List[str]], 
            timeout: Optional[float] = None,
            cwd: Optional[Union[str, Path]] = None,
            env: Optional[Dict[str, str]] = None,
            check: bool = False,
            shell: bool = True,
            capture_output: bool = True,
            text: bool = True,
            encoding: str = 'utf-8',
            input_data: Optional[str] = None,
            progress_callback: Optional[Callable[[str], None]] = None) -> CaptureResult:
        """
        Execute a command and capture its output.
        
        Args:
            command: Command to execute (string or list of arguments)
            timeout: Timeout in seconds (overrides default)
            cwd: Working directory (overrides default)
            env: Environment variables (merged with default)
            check: If True, raise CommandError on non-zero exit code
            shell: If True, execute through shell
            capture_output: If True, capture stdout and stderr
            text: If True, decode output as text
            encoding: Text encoding to use
            input_data: Data to send to stdin
            progress_callback: Callback function for real-time output
            
        Returns:
            CaptureResult object with execution details
            
        Raises:
            CommandError: If command fails and check=True
            TimeoutError: If command times out
        """
        # Prepare command
        if isinstance(command, str):
            if not shell:
                command = split_command(command)
        
        # Set up environment
        final_env = self.default_env.copy()
        if env:
            final_env.update(env)
        
        # Set working directory
        final_cwd = cwd or self.default_cwd
        if final_cwd:
            final_cwd = Path(final_cwd)
        
        # Set timeout
        final_timeout = timeout if timeout is not None else self.default_timeout
        
        # Record start time
        start_time = time.time()
        
        try:
            # Create subprocess
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE if capture_output else None,
                stderr=subprocess.PIPE if capture_output else None,
                stdin=subprocess.PIPE if input_data else None,
                cwd=final_cwd,
                env=final_env if final_env else None,
                shell=shell,
                text=text,
                encoding=encoding if text else None
            )
            
            # Handle real-time output if callback provided
            stdout_data = ""
            stderr_data = ""
            
            if progress_callback and capture_output:
                stdout_data, stderr_data = self._handle_realtime_output(
                    process, progress_callback, final_timeout, input_data
                )
            else:
                # Standard communication
                try:
                    stdout_data, stderr_data = process.communicate(
                        input=input_data, timeout=final_timeout
                    )
                except subprocess.TimeoutExpired:
                    process.kill()
                    stdout_data, stderr_data = process.communicate()
                    execution_time = time.time() - start_time
                    raise TimeoutError(
                        f"Command '{command}' timed out after {final_timeout} seconds",
                        timeout=final_timeout,
                        command=str(command)
                    )
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Create result
            result = CaptureResult(
                command=str(command),
                return_code=process.returncode,
                stdout=stdout_data or "",
                stderr=stderr_data or "",
                execution_time=execution_time,
                success=process.returncode == 0,
                pid=process.pid
            )
            
            # Check for errors if requested
            if check and not result.success:
                raise CommandError(
                    f"Command '{command}' failed with return code {result.return_code}",
                    return_code=result.return_code,
                    command=str(command)
                )
            
            return result
            
        except (FileNotFoundError, PermissionError) as e:
            execution_time = time.time() - start_time
            raise CommandError(
                f"Failed to execute command '{command}': {str(e)}",
                command=str(command)
            )
    
    def _handle_realtime_output(self, process, callback, timeout, input_data):
        """Handle real-time output with progress callback."""
        stdout_lines = []
        stderr_lines = []
        
        def read_output(pipe, lines_list, callback_func):
            for line in iter(pipe.readline, ''):
                if line:
                    lines_list.append(line)
                    if callback_func:
                        callback_func(line.rstrip())
        
        # Start output reading threads
        stdout_thread = threading.Thread(
            target=read_output, 
            args=(process.stdout, stdout_lines, callback)
        )
        stderr_thread = threading.Thread(
            target=read_output, 
            args=(process.stderr, stderr_lines, None)
        )
        
        stdout_thread.start()
        stderr_thread.start()
        
        # Send input if provided
        if input_data:
            process.stdin.write(input_data)
            process.stdin.close()
        
        # Wait for process completion with timeout
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            raise TimeoutError(
                f"Command timed out after {timeout} seconds",
                timeout=timeout
            )
        
        # Wait for output threads to complete
        stdout_thread.join()
        stderr_thread.join()
        
        return ''.join(stdout_lines), ''.join(stderr_lines)
    
    def run_async(self, command: Union[str, List[str]], **kwargs) -> subprocess.Popen:
        """
        Execute a command asynchronously and return the process object.
        
        Args:
            command: Command to execute
            **kwargs: Additional arguments passed to subprocess.Popen
            
        Returns:
            subprocess.Popen object
        """
        if isinstance(command, str):
            command = split_command(command)
        
        return subprocess.Popen(command, **kwargs)
    
    def run_multiple(self, commands: List[Union[str, List[str]]], 
                    parallel: bool = False, **kwargs) -> List[CaptureResult]:
        """
        Execute multiple commands.
        
        Args:
            commands: List of commands to execute
            parallel: If True, run commands in parallel
            **kwargs: Additional arguments passed to run()
            
        Returns:
            List of CaptureResult objects
        """
        if not parallel:
            return [self.run(cmd, **kwargs) for cmd in commands]
        
        # Parallel execution
        import concurrent.futures
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.run, cmd, **kwargs) for cmd in commands]
            return [future.result() for future in concurrent.futures.as_completed(futures)]
    
    def which(self, command: str) -> Optional[str]:
        """Find the full path to a command."""
        return is_command_available(command)
    
    def is_available(self, command: str) -> bool:
        """Check if a command is available."""
        return is_command_available(command) 