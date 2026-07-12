import os


def compile_snapshot():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    snapshot_path = os.path.join(project_root, "docs", "LLM_SNAPSHOT.md")

    files_to_include = [
        "pyproject.toml",
        "requirements.txt",
        ".pre-commit-config.yaml",
        "code-security.datadog.yaml",
        "src/pipeline/__init__.py",
        "src/pipeline/main.py",
        "src/pipeline/models.py",
        "src/pipeline/parser.py",
        "src/pipeline/api.py",
        "tests/__init__.py",
        "tests/test_models.py",
        "tests/test_api.py",
        "tests/test_adversarial_boundaries.py",
    ]

    with open(snapshot_path, "w", encoding="utf-8") as out:
        out.write("# EthoPipe Codebase Snapshot\n\n")
        out.write(
            "This file is auto-generated on git push. It aggregates all "
            "configuration and first-party Python source files into a single "
            "context file.\n\n"
        )

        for relative_path in files_to_include:
            full_path = os.path.join(project_root, relative_path)
            if not os.path.exists(full_path):
                continue

            out.write(f"## File: `{relative_path}`\n\n")

            # Determine syntax highlighting language
            ext = os.path.splitext(relative_path)[1]
            lang = "python"
            if ext == ".toml":
                lang = "toml"
            elif ext in [".yaml", ".yml"]:
                lang = "yaml"
            elif ext == ".txt":
                lang = "text"

            out.write(f"```{lang}\n")
            with open(full_path, encoding="utf-8") as f:
                out.write(f.read())
            if not file_ends_with_newline(full_path):
                out.write("\n")
            out.write("```\n\n")


def file_ends_with_newline(filepath):
    try:
        with open(filepath, "rb") as f:
            f.seek(-1, os.SEEK_END)
            return f.read(1) == b"\n"
    except Exception:
        return True


if __name__ == "__main__":
    compile_snapshot()
