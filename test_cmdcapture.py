#!/usr/bin/env python3
"""
Basic tests for the Command Capture library.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the package to the path for testing
sys.path.insert(0, str(Path(__file__).parent))

from cmdcapture import CommandCapture, CommandError, TimeoutError


def test_basic_command():
    """Test basic command execution."""
    capture = CommandCapture()
    result = capture.run("echo 'test'")
    
    assert result.success
    assert result.return_code == 0
    assert "test" in result.stdout
    assert result.execution_time > 0
    print("✓ Basic command test passed")


def test_command_with_error():
    """Test command that returns non-zero exit code."""
    capture = CommandCapture()
    result = capture.run("ls /nonexistent_directory")
    
    assert not result.success
    assert result.return_code != 0
    assert len(result.stderr) > 0
    print("✓ Command error test passed")


def test_command_with_check():
    """Test command with check=True raises exception on error."""
    capture = CommandCapture()
    
    try:
        result = capture.run("ls /nonexistent_directory", check=True)
        assert False, "Should have raised CommandError"
    except CommandError as e:
        assert e.return_code != 0
        print("✓ Command check test passed")


def test_timeout():
    """Test command timeout."""
    capture = CommandCapture()
    
    try:
        result = capture.run("sleep 2", timeout=0.5)
        assert False, "Should have raised TimeoutError"
    except TimeoutError as e:
        assert e.timeout == 0.5
        print("✓ Timeout test passed")


def test_working_directory():
    """Test setting working directory."""
    capture = CommandCapture()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        result = capture.run("pwd", cwd=temp_dir)
        assert temp_dir in result.stdout
        print("✓ Working directory test passed")


def test_environment_variables():
    """Test environment variables."""
    capture = CommandCapture()
    result = capture.run("echo $TEST_VAR", env={"TEST_VAR": "test_value"})
    
    assert "test_value" in result.stdout
    print("✓ Environment variables test passed")


def test_input_data():
    """Test sending input data to command."""
    capture = CommandCapture()
    result = capture.run("cat", input_data="hello world")
    
    assert "hello world" in result.stdout
    print("✓ Input data test passed")


def test_multiple_commands():
    """Test running multiple commands."""
    capture = CommandCapture()
    commands = ["echo 'first'", "echo 'second'", "echo 'third'"]
    results = capture.run_multiple(commands)
    
    assert len(results) == 3
    assert all(r.success for r in results)
    assert "first" in results[0].stdout
    assert "second" in results[1].stdout
    assert "third" in results[2].stdout
    print("✓ Multiple commands test passed")


def test_command_availability():
    """Test checking command availability."""
    capture = CommandCapture()
    
    # These commands should be available on most systems
    assert capture.is_available("echo")
    assert capture.is_available("ls") or capture.is_available("dir")  # Windows compatibility
    
    # This command should not exist
    assert not capture.is_available("definitely_nonexistent_command_12345")
    print("✓ Command availability test passed")


def test_capture_result_properties():
    """Test CaptureResult properties."""
    capture = CommandCapture()
    result = capture.run("echo 'test'")
    
    assert hasattr(result, 'command')
    assert hasattr(result, 'return_code')
    assert hasattr(result, 'stdout')
    assert hasattr(result, 'stderr')
    assert hasattr(result, 'execution_time')
    assert hasattr(result, 'success')
    assert hasattr(result, 'pid')
    
    # Test string representation
    str_repr = str(result)
    assert "CaptureResult" in str_repr
    assert result.command in str_repr
    print("✓ CaptureResult properties test passed")


def run_all_tests():
    """Run all tests."""
    print("Running Command Capture Library Tests...\n")
    
    tests = [
        test_basic_command,
        test_command_with_error,
        test_command_with_check,
        test_timeout,
        test_working_directory,
        test_environment_variables,
        test_input_data,
        test_multiple_commands,
        test_command_availability,
        test_capture_result_properties,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print(f"\nTest Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 