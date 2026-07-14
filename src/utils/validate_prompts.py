import re
import sys

from src.pipeline.models import PROHIBITED_WORDS


def main():
    files = sys.argv[1:]
    has_errors = False

    # Pattern to find prohibited words as full words, case-insensitive
    pattern = re.compile(rf"\b({'|'.join(PROHIBITED_WORDS)})\b", re.IGNORECASE)

    for filepath in files:
        try:
            with open(filepath, encoding="utf-8") as f:
                content = f.read()

            # Skip checking models.py because it defines the prohibited words
            if "models.py" in filepath:
                continue

            matches = pattern.findall(content)
            if matches:
                print(
                    f"Error: {filepath} has subjective terms: {set(matches)}.\n"
                    "Linguistic objectivity requires filtering these words.",
                    file=sys.stderr,
                )
                has_errors = True
        except Exception as e:
            print(f"Error reading {filepath}: {e}", file=sys.stderr)
            has_errors = True

    if has_errors:
        sys.exit(1)
    print("Prompt structure validation passed.")


if __name__ == "__main__":
    main()
