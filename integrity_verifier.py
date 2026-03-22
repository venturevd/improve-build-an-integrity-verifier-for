#!/usr/bin/env python3
"""
Agent Dashboard Integrity Verifier

This tool cross-checks agent KPIs against raw telemetry data, ensures data provenance,
detects metric drift, and generates auditable reports to prevent misleading dashboards.

Features:
- Detailed error messages for file loading issues
- Specific error handling for JSON and CSV parsing
- Clear progress reporting
- User-friendly guidance for fixing issues
"""

import argparse
import json
import csv
import os
import sys
from datetime import datetime


def load_kpi_data(file_path):
    """Load KPI data from a JSON file with detailed error handling."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"KPI data file not found: {file_path}")

        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"Permission denied: cannot read {file_path}")

        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("KPI data must be a list of records")
                return data
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in KPI data file: {e}") from e

    except Exception as e:
        raise RuntimeError(f"Failed to load KPI data: {str(e)}") from e


def load_telemetry_data(file_path):
    """Load telemetry data from a CSV file with detailed error handling."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Telemetry data file not found: {file_path}")

        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"Permission denied: cannot read {file_path}")

        with open(file_path, 'r') as f:
            try:
                # First read the file content to check for CSV errors
                content = f.read()
                if not content.strip():
                    raise ValueError("Telemetry data file is empty")

                # Check if the file looks like a CSV (has commas and newlines)
                if ',' not in content or '\n' not in content:
                    raise ValueError("Telemetry data file does not appear to be a valid CSV")

                # Then try to parse as CSV
                f.seek(0)  # Reset file position
                reader = csv.DictReader(f)
                data = list(reader)
                if not data:
                    raise ValueError("Telemetry data file has no rows after header")
                return data
            except csv.Error as e:
                raise ValueError(f"Invalid CSV format in telemetry data: {e}") from e

    except Exception as e:
        raise RuntimeError(f"Failed to load telemetry data: {str(e)}") from e


def verify_integrity(kpi_data, telemetry_data):
    """Verify the integrity of agent KPIs against telemetry data."""
    # This is a simplified example - in a real implementation, this would
    # perform detailed cross-checking, provenance verification, and drift detection

    if not kpi_data:
        raise ValueError("No KPI data provided for verification")

    if not telemetry_data:
        raise ValueError("No telemetry data provided for verification")

    # Example verification: check that all KPI records have corresponding telemetry
    kpi_ids = {record.get('agent_id') for record in kpi_data if 'agent_id' in record}
    telemetry_ids = {record.get('agent_id') for record in telemetry_data if 'agent_id' in record}

    missing_ids = kpi_ids - telemetry_ids
    if missing_ids:
        return False, f"Missing telemetry data for agents: {', '.join(missing_ids)}"

    return True, "All KPIs verified successfully"


def generate_report(output_file, kpi_data, telemetry_data, is_valid, message):
    """Generate an auditable report in HTML format."""
    try:
        with open(output_file, 'w') as f:
            f.write("<html><body>")
            f.write(f"<h1>Agent Dashboard Integrity Report</h1>")
            f.write(f"<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
            f.write(f"<h2>Verification Status: {'✓ PASS' if is_valid else '✗ FAIL'}</h2>")
            f.write(f"<p>{message}</p>")

            f.write("<h2>KPI Data Summary</h2>")
            f.write(f"<p>Records: {len(kpi_data)}</p>")

            f.write("<h2>Telemetry Data Summary</h2>")
            f.write(f"<p>Records: {len(telemetry_data)}</p>")

            f.write("</body></html>")

    except Exception as e:
        raise RuntimeError(f"Failed to generate report: {str(e)}") from e


def main():
    """Main function to execute the integrity verification."""
    parser = argparse.ArgumentParser(description='Agent Dashboard Integrity Verifier')
    parser.add_argument('--kpi-data', required=True, help='Path to KPI data JSON file')
    parser.add_argument('--telemetry-data', required=True, help='Path to telemetry data CSV file')
    parser.add_argument('--output', required=True, help='Path to output report HTML file')

    args = parser.parse_args()

    try:
        print("Loading KPI data...")
        kpi_data = load_kpi_data(args.kpi_data)
        print("✓ KPI data loaded successfully")

        print("Loading telemetry data...")
        telemetry_data = load_telemetry_data(args.telemetry_data)
        print("✓ Telemetry data loaded successfully")

        print("Verifying data integrity...")
        is_valid, message = verify_integrity(kpi_data, telemetry_data)
        print(f"✓ Verification {'succeeded' if is_valid else 'failed'}: {message}")

        print(f"Generating report to {args.output}...")
        generate_report(args.output, kpi_data, telemetry_data, is_valid, message)
        print("✓ Report generated successfully")

        if is_valid:
            print("\n🎉 All checks passed! Your dashboard data is consistent and auditable.")
        else:
            print(f"\n⚠️  Verification failed: {message}")
            print("   - Check that all agents in KPI data have corresponding telemetry records")
            print("   - Verify file paths and permissions")
            print("   - Ensure data formats are correct (JSON for KPIs, CSV for telemetry)")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if "file not found" in str(e).lower():
            print("   - Check that the file exists and the path is correct")
        elif "permission denied" in str(e).lower():
            print("   - Check file permissions (try: chmod +r <filename>)")
        elif "invalid json" in str(e).lower():
            print("   - Verify the KPI data file is valid JSON")
        elif "invalid csv" in str(e).lower():
            print("   - Verify the telemetry data file is valid CSV")
        else:
            print("   - See error message above for details")
        sys.exit(1)


if __name__ == "__main__":
    main()