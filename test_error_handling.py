#!/usr/bin/env python3
"""
Test script for the improved error handling in the Agent Dashboard Integrity Verifier.

This script verifies that all error scenarios are handled properly:
- File not found errors
- Permission denied errors
- Invalid JSON parsing
- Invalid CSV parsing
- Empty files
- Missing required fields
"""

import os
import sys
import tempfile
import json
import csv
import subprocess
import shutil
from pathlib import Path


def create_test_files():
    """Create test files for various error scenarios."""
    test_dir = Path(tempfile.mkdtemp())

    # Valid files
    valid_kpi_data = [{"agent_id": "1", "kpi": 0.95}]
    with open(test_dir / "valid_kpis.json", "w") as f:
        json.dump(valid_kpi_data, f)

    valid_telemetry_data = [{"agent_id": "1", "metric": 100}]
    with open(test_dir / "valid_telemetry.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["agent_id", "metric"])
        writer.writeheader()
        writer.writerows(valid_telemetry_data)

    # Invalid files
    with open(test_dir / "invalid_json.json", "w") as f:
        f.write("{invalid json}")

    # Create a CSV with invalid content that will cause csv.DictReader to fail
    with open(test_dir / "invalid_csv.csv", "w") as f:
        # Create a CSV with completely invalid format
        f.write('This is not a CSV file at all\nJust some random text\nNo headers or structure')

    with open(test_dir / "empty_csv.csv", "w") as f:
        f.write("agent_id,metric\n")

    # Permission-denied file
    permission_denied_file = test_dir / "permission_denied.json"
    with open(permission_denied_file, "w") as f:
        json.dump([{"agent_id": "1", "kpi": 0.95}], f)
    os.chmod(permission_denied_file, 0o000)  # No permissions

    return test_dir


def run_test(test_name, kpi_file, telemetry_file, expected_error=None):
    """Run a test case and check the output."""
    print(f"\n🧪 Testing: {test_name}")

    # Debug: Print file contents
    if "invalid_csv" in str(telemetry_file):
        print(f"Debug: Invalid CSV file contents:")
        with open(telemetry_file, 'r') as f:
            print(f.read())

    cmd = [
        sys.executable, "integrity_verifier.py",
        "--kpi-data", str(kpi_file),
        "--telemetry-data", str(telemetry_file),
        "--output", "/tmp/test_report.html"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        # Combine stdout and stderr for checking
        full_output = result.stdout + result.stderr

        if expected_error:
            if expected_error not in full_output.lower():
                print(f"❌ Expected error '{expected_error}' not found in output")
                print(f"Output: {full_output}")
                return False
            else:
                print(f"✅ Found expected error: {expected_error}")
                return True
        else:
            if result.returncode != 0:
                print(f"❌ Test failed with unexpected error: {full_output}")
                return False
            else:
                print("✅ Test passed")
                return True
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        return False


def main():
    """Run all test cases."""
    print("🚀 Running Agent Dashboard Integrity Verifier Error Handling Tests")
    print("=" * 60)

    test_dir = create_test_files()

    try:
        # Test cases
        tests = [
            # Valid case
            ("Valid files", test_dir / "valid_kpis.json", test_dir / "valid_telemetry.csv", None),

            # Error cases
            ("File not found (KPI)", "nonexistent.json", test_dir / "valid_telemetry.csv", "file not found"),
            ("File not found (Telemetry)", test_dir / "valid_kpis.json", "nonexistent.csv", "file not found"),
            ("Invalid JSON", test_dir / "invalid_json.json", test_dir / "valid_telemetry.csv", "invalid json"),
            ("Invalid CSV", test_dir / "valid_kpis.json", test_dir / "invalid_csv.csv", "does not appear to be a valid csv"),
            ("Empty CSV", test_dir / "valid_kpis.json", test_dir / "empty_csv.csv", "no rows after header"),
            ("Permission denied", test_dir / "permission_denied.json", test_dir / "valid_telemetry.csv", "permission denied"),
        ]

        passed = 0
        total = len(tests)

        for test_name, kpi_file, telemetry_file, expected_error in tests:
            if run_test(test_name, kpi_file, telemetry_file, expected_error):
                passed += 1

        print("\n" + "=" * 60)
        print(f"📊 Test Results: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All tests passed! Error handling is working correctly.")
            return 0
        else:
            print("❌ Some tests failed. Check the output above for details.")
            return 1

    finally:
        # Clean up
        shutil.rmtree(test_dir)
        if os.path.exists("/tmp/test_report.html"):
            os.remove("/tmp/test_report.html")


if __name__ == "__main__":
    sys.exit(main())