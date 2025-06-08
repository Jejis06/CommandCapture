"""
Command-line interface for the Command Capture library.
"""

import argparse
import json
import sys
from typing import Optional

from .core import CommandCapture
from .exceptions import CommandError, TimeoutError


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Capture output from terminal commands",
        prog="cmdcapture"
    )
    
    parser.add_argument(
        "command",
        help="Command to execute"
    )
    
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        help="Timeout in seconds"
    )
    
    parser.add_argument(
        "-d", "--cwd",
        help="Working directory"
    )
    
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit with error code if command fails"
    )
    
    parser.add_argument(
        "--no-shell",
        action="store_true",
        help="Don't execute through shell"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON"
    )
    
    parser.add_argument(
        "-i", "--input",
        help="Data to send to stdin"
    )
    
    parser.add_argument(
        "--progress",
        action="store_true",
        help="Show real-time output"
    )
    
    args = parser.parse_args()
    
    # Create CommandCapture instance
    capture = CommandCapture(
        default_timeout=args.timeout,
        default_cwd=args.cwd
    )
    
    # Progress callback
    progress_callback = None
    if args.progress:
        def progress_callback(line):
            print(f"[PROGRESS] {line}", file=sys.stderr)
    
    try:
        # Execute command
        result = capture.run(
            args.command,
            timeout=args.timeout,
            cwd=args.cwd,
            check=args.check,
            shell=not args.no_shell,
            input_data=args.input,
            progress_callback=progress_callback
        )
        
        if args.json:
            # Output as JSON
            output = {
                "command": result.command,
                "return_code": result.return_code,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "execution_time": result.execution_time,
                "success": result.success,
                "pid": result.pid
            }
            print(json.dumps(output, indent=2))
        else:
            # Standard output
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, end="", file=sys.stderr)
        
        # Exit with command's return code
        sys.exit(result.return_code)
        
    except (CommandError, TimeoutError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main() 