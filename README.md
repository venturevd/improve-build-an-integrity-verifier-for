# Integrity Verifier with Detailed Error Messages

This tool enhances the agent dashboard integrity verifier by providing more detailed error messages when files can't be read.

## Features
- Cross-checks agent KPIs against raw telemetry
- Ensures data provenance
- Detects metric drift
- Generates auditable reports to prevent misleading dashboards
- Provides detailed error messages for file reading issues

## Installation

This project requires Python 3.6 or higher. No additional dependencies are needed beyond the standard library.

## Usage

```bash
python3 main.py <file_path>
```

Replace `<file_path>` with the path to the file you want to read.

## Example

```bash
python3 main.py /path/to/your/file.txt
```

## Error Handling

The tool provides detailed error messages for various file reading issues:
- File not found
- Permission denied
- Other I/O errors

Each error message includes:
- The file path
- The error type
- The specific error message

## License

This project is licensed under the MIT License.