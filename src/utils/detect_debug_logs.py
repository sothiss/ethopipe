import re
import sys


def main():
    files = sys.argv[1:]
    has_errors = False

    # Check for direct configuration of DEBUG/INFO log levels
    debug_pattern = re.compile(r"logging\.(DEBUG|INFO)")

    for filepath in files:
        try:
            with open(filepath, encoding="utf-8") as f:
                content = f.read()

            # Scan for occurrences of logging.DEBUG or logging.INFO
            matches = debug_pattern.findall(content)
            if matches:
                print(
                    f"Error: {filepath} has debug/info logs: {matches}.\n"
                    "Ensure log level is set to CRITICAL for production.",
                    file=sys.stderr,
                )
                has_errors = True
        except Exception as e:
            print(f"Error reading {filepath}: {e}", file=sys.stderr)
            has_errors = True

    if has_errors:
        sys.exit(1)
    print("Log level check passed.")


if __name__ == "__main__":
    main()
