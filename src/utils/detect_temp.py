import re
import sys


def main():
    files = sys.argv[1:]
    has_errors = False

    # Pattern to match temperature setting (e.g., temperature=0.7 or temperature = 0.5)
    temp_pattern = re.compile(r"temperature\s*=\s*([0-9.]+)")

    for filepath in files:
        try:
            with open(filepath, encoding="utf-8") as f:
                content = f.read()

            matches = temp_pattern.findall(content)
            for val in matches:
                try:
                    temp_val = float(val)
                    if temp_val > 0.0:
                        print(
                            f"Error: {filepath} sets temperature={temp_val}.\n"
                            "Must be set strictly to 0.0 to prevent variance.",
                            file=sys.stderr,
                        )
                        has_errors = True
                except ValueError:
                    pass
        except Exception as e:
            print(f"Error reading {filepath}: {e}", file=sys.stderr)
            has_errors = True

    if has_errors:
        sys.exit(1)
    print("Temperature check passed.")


if __name__ == "__main__":
    main()
