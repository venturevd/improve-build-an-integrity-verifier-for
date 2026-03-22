import os
import sys
import argparse

def read_file(file_path):
    """Read a file and return its contents.

    Args:
        file_path (str): Path to the file to read.

    Returns:
        str: Contents of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read due to permission issues.
        IOError: For other I/O related errors.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"Permission denied: {file_path}")

        with open(file_path, 'r') as file:
            return file.read()

    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        raise IOError(f"Error reading file '{file_path}': [{error_type}] {error_msg}") from e

def main():
    parser = argparse.ArgumentParser(description='Integrity Verifier with Detailed Error Messages')
    parser.add_argument('file_path', type=str, help='Path to the file to read')
    args = parser.parse_args()

    try:
        content = read_file(args.file_path)
        print("File content:")
        print(content)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()