import subprocess
import sys
import os
import pytest

def run_cli(args):
    """Helper to run the CLI agent script with given args and return output."""
    cmd = [sys.executable, 'cli_agent.py'] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

def test_cli_generate_code():
    result = run_cli(['generate', '--task', 'Write a Python function to add two numbers'])
    assert result.returncode == 0
    assert 'def' in result.stdout
    assert 'add' in result.stdout

def test_cli_review_code():
    code = 'def add(a, b): return a + b'
    result = run_cli(['review', '--code', code])
    assert result.returncode == 0
    assert 'review' in result.stdout.lower() or 'improvement' in result.stdout.lower() or 'bug' in result.stdout.lower()
