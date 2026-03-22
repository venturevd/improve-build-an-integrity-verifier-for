# Improve: Build an Integrity Verifier for Agent Dashboards

This project enhances the existing agent dashboard integrity verifier by adding more detailed error messages when files can't be read.

## Overview

The original integrity verifier tool cross-checks agent KPIs against raw telemetry data, ensures data provenance, detects metric drift, and generates auditable reports. This improvement focuses on enhancing the error handling to provide more actionable feedback to users.

## Key Improvements

1. **Detailed Error Messages**:
   - Clear indication of which file couldn't be read
   - Specific error types (file not found, permission denied, parsing errors)
   - Contextual information to help users fix issues

2. **Enhanced File Loading Functions**:
   - `load_kpi_data()` now provides detailed JSON parsing errors
   - `load_telemetry_data()` now provides detailed CSV parsing errors
   - Both functions handle permission and file not found errors explicitly

3. **Improved Main Function**:
   - Better progress reporting
   - Clear error handling and display
   - User-friendly guidance for fixing issues

4. **Comprehensive Testing**:
   - Added test script for various error scenarios
   - Verifies all error handling paths
   - Ensures successful file loading still works

## Files Modified

1. `integrity_verifier.py` - Enhanced error handling in file loading functions and main execution
2. `README.md` - Updated documentation to include error handling improvements
3. `test_error_handling.py` - Added comprehensive test script for error scenarios

## Usage

The improved tool can be used exactly like the original:

```bash
python3 integrity_verifier.py \
  --kpi-data kpis.json \
  --telemetry-data telemetry.csv \
  --output report.html
```

But now provides much better error messages when things go wrong.

### Sample Files

Sample KPI and telemetry files are included for testing:
- `sample_kpis.json` - Example KPI data
- `sample_telemetry.csv` - Example telemetry data

You can run the tool with these samples:

```bash
python3 integrity_verifier.py \
  --kpi-data sample_kpis.json \
  --telemetry-data sample_telemetry.csv \
  --output sample_report.html
```

## Testing

To test the improved error handling:

```bash
python3 test_error_handling.py
```

This will verify that all error scenarios are handled properly, including:
- File not found errors
- Permission denied errors
- Invalid JSON parsing
- Invalid CSV parsing
- Empty files
- Missing required fields

## Requirements

- Python 3.8+
- pandas
- numpy
- requests

Install dependencies with:

```bash
pip install -r requirements.txt
```