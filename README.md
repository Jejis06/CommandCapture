# Command Capture Library

A comprehensive Python library for capturing output from terminal commands with advanced features including timeouts, real-time output, parallel execution, and more.

## Features

- 🚀 **Simple and intuitive API** - Easy to use for basic command execution
- ⏱️ **Timeout support** - Prevent commands from running indefinitely
- 🔄 **Real-time output** - Stream command output as it happens
- 🏃 **Parallel execution** - Run multiple commands simultaneously
- 🌍 **Environment control** - Set custom environment variables
- 📁 **Working directory** - Execute commands in specific directories
- 💾 **Input/Output handling** - Send input to commands and capture all output
- 🛡️ **Error handling** - Comprehensive error handling with custom exceptions
- 📊 **Detailed results** - Rich result objects with execution metadata
- 🖥️ **Cross-platform** - Works on Linux, macOS, and Windows
- 📦 **Zero dependencies** - Uses only Python standard library

## Installation

### From source
```bash
git clone <repository-url>
cd cmdcapture
pip install .
```

### For development
```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from cmdcapture import CommandCapture

# Create a CommandCapture instance
capture = CommandCapture()

# Execute a simple command
result = capture.run("echo 'Hello, World!'")
print(result.stdout)  # Hello, World!
print(result.success)  # True
print(result.return_code)  # 0
```

## Basic Usage

### Simple Command Execution
```python
from cmdcapture import CommandCapture

capture = CommandCapture()
result = capture.run("ls -la")

if result.success:
    print("Command succeeded!")
    print(result.stdout)
else:
    print(f"Command failed with return code: {result.return_code}")
    print(result.stderr)
```

### Error Handling
```python
from cmdcapture import CommandCapture, CommandError

capture = CommandCapture()
try:
    # Use check=True to raise exception on command failure
    result = capture.run("ls /nonexistent", check=True)
except CommandError as e:
    print(f"Command failed: {e}")
    print(f"Return code: {e.return_code}")
```

### Timeout Support
```python
from cmdcapture import CommandCapture, TimeoutError

capture = CommandCapture()
try:
    result = capture.run("sleep 10", timeout=5.0)
except TimeoutError as e:
    print(f"Command timed out after {e.timeout} seconds")
```

## Advanced Features

### Real-time Output
```python
def progress_callback(line):
    print(f"[OUTPUT] {line}")

result = capture.run("ping -c 3 google.com", progress_callback=progress_callback)
```

### Environment Variables
```python
result = capture.run("echo $MY_VAR", env={"MY_VAR": "Hello World"})
print(result.stdout)  # Hello World
```

### Working Directory
```python
result = capture.run("pwd", cwd="/tmp")
print(result.stdout)  # /tmp (or equivalent)
```

### Input Data
```python
result = capture.run("grep 'pattern'", input_data="line with pattern\nother line")
print(result.stdout)  # line with pattern
```

### Multiple Commands
```python
# Sequential execution
commands = ["echo 'first'", "echo 'second'", "echo 'third'"]
results = capture.run_multiple(commands)

# Parallel execution
results = capture.run_multiple(commands, parallel=True)
```

### Command Availability
```python
if capture.is_available("git"):
    result = capture.run("git --version")
    print(result.stdout)
else:
    print("Git is not available")
```

## Command Line Interface

The library also provides a CLI interface:

```bash
# Basic usage
cmdcapture "echo 'Hello, World!'"

# With JSON output
cmdcapture "ls -la" --json

# With timeout
cmdcapture "sleep 5" --timeout 2

# With working directory
cmdcapture "pwd" --cwd /tmp

# Send input
cmdcapture "cat" --input "Hello, World!"
```

## API Reference

### CommandCapture

Main class for executing commands.

#### Constructor
```python
CommandCapture(
    default_timeout: Optional[float] = None,
    default_cwd: Optional[Union[str, Path]] = None,
    default_env: Optional[Dict[str, str]] = None
)
```

#### Methods

**`run(command, **kwargs) -> CaptureResult`**

Execute a command and return results.

Parameters:
- `command`: Command to execute (string or list)
- `timeout`: Timeout in seconds
- `cwd`: Working directory
- `env`: Environment variables
- `check`: Raise exception on command failure
- `shell`: Execute through shell (default: True)
- `input_data`: Data to send to stdin
- `progress_callback`: Function to call with real-time output

**`run_multiple(commands, parallel=False, **kwargs) -> List[CaptureResult]`**

Execute multiple commands.

**`is_available(command) -> bool`**

Check if a command is available in the system PATH.

### CaptureResult

Result object containing command execution details.

Attributes:
- `command`: The executed command
- `return_code`: Exit code
- `stdout`: Standard output
- `stderr`: Standard error output
- `execution_time`: Execution time in seconds
- `success`: Boolean indicating success (return_code == 0)
- `pid`: Process ID

### Exceptions

**`CommandError`**: Raised when command execution fails (when `check=True`)
**`TimeoutError`**: Raised when command execution times out

## Testing

Run the test suite:

```bash
python test_cmdcapture.py
```

Run the examples:

```bash
python example.py
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 