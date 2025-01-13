import pytest
import io
import sys

def run_tests():
    # Capture the output
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    # Run the tests
    pytest.main(["-q", "--tb=short", "--disable-warnings"])

    # Restore stdout
    sys.stdout = old_stdout
    output = new_stdout.getvalue()

    return output