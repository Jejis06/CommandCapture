#!/usr/bin/env python3
"""
Example usage of the Command Capture library.
"""

import time
from cmdcapture import CommandCapture, CommandError, TimeoutError

def main():
    print("=== Command Capture Library Examples ===\n")
    
    # Create a CommandCapture instance
    capture = CommandCapture()
    
    # Example 1: Basic command execution
    print("1. Basic command execution:")
    result = capture.run("echo 'Hello, World!'")
    print(f"Command: {result.command}")
    print(f"Output: {result.stdout.strip()}")
    print(f"Success: {result.success}")
    print(f"Execution time: {result.execution_time:.3f}s\n")
    
    # Example 2: Command with error handling
    print("2. Command with error (non-zero exit code):")
    try:
        result = capture.run("ls /nonexistent_directory", check=True)
    except CommandError as e:
        print(f"Caught CommandError: {e}")
        print(f"Return code: {e.return_code}\n")
    
    # Example 3: Command with timeout
    print("3. Command with timeout:")
    try:
        result = capture.run("sleep 3", timeout=1.0)
    except TimeoutError as e:
        print(f"Caught TimeoutError: {e}")
        print(f"Timeout: {e.timeout}s\n")
    
    # Example 4: Capture both stdout and stderr
    print("4. Capturing stdout and stderr:")
    result = capture.run("python3 -c \"import sys; print('stdout'); print('stderr', file=sys.stderr)\"")
    print(f"Stdout: {repr(result.stdout)}")
    print(f"Stderr: {repr(result.stderr)}")
    print()
    
    # Example 5: Working directory
    print("5. Setting working directory:")
    result = capture.run("pwd", cwd="/tmp")
    print(f"Working directory: {result.stdout.strip()}\n")
    
    # Example 6: Environment variables
    print("6. Environment variables:")
    result = capture.run("echo $CUSTOM_VAR", env={"CUSTOM_VAR": "Hello from env!"})
    print(f"Environment variable: {result.stdout.strip()}\n")
    
    # Example 7: Real-time output with callback
    print("7. Real-time output (simulated with echo):")
    def progress_callback(line):
        print(f"[PROGRESS] {line}")
    
    result = capture.run(
        "python3 -c \"import time; [print(f'Line {i}') or time.sleep(0.1) for i in range(3)]\"",
        progress_callback=progress_callback
    )
    print("Real-time output completed\n")
    
    # Example 8: Multiple commands
    print("8. Multiple commands (sequential):")
    commands = ["echo 'First'", "echo 'Second'", "echo 'Third'"]
    results = capture.run_multiple(commands)
    for i, result in enumerate(results):
        print(f"Command {i+1}: {result.stdout.strip()}")
    print()
    
    # Example 9: Multiple commands (parallel)
    print("9. Multiple commands (parallel):")
    commands = ["sleep 1 && echo 'First'", "sleep 1 && echo 'Second'", "sleep 1 && echo 'Third'"]
    start_time = time.time()
    results = capture.run_multiple(commands, parallel=True)
    end_time = time.time()
    for i, result in enumerate(results):
        print(f"Command {i+1}: {result.stdout.strip()}")
    print(f"Total time (parallel): {end_time - start_time:.2f}s\n")
    
    # Example 10: Check command availability
    print("10. Check command availability:")
    commands_to_check = ["python3", "git", "nonexistent_command"]
    for cmd in commands_to_check:
        available = capture.is_available(cmd)
        print(f"{cmd}: {'Available' if available else 'Not available'}")
    print()
    
    # Example 11: Input data
    print("11. Sending input to command:")
    result = capture.run("python3 -c \"import sys; print(f'You said: {sys.stdin.read().strip()}')\"", 
                        input_data="Hello from input!")
    print(f"Result: {result.stdout.strip()}\n")
    
    # Example 12: Different output formats
    print("12. Command result details:")
    result = capture.run("date")
    print(f"Command: {result.command}")
    print(f"Return code: {result.return_code}")
    print(f"Success: {result.success}")
    print(f"PID: {result.pid}")
    print(f"Execution time: {result.execution_time:.3f}s")
    print(f"Output length: {len(result.stdout)} chars")
    print(f"Result object: {result}")


if __name__ == "__main__":
    main() 