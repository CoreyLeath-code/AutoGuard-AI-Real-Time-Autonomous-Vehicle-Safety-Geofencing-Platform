"""Generate a descriptive repository-inventory table for workflow summaries.

This script intentionally does not measure performance, safety, accuracy, or
production readiness. It only counts selected tracked text-file contents in the
current checkout.
"""

from __future__ import annotations

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TARGET_EXTENSIONS = (".py", ".json", ".yaml", ".yml", ".md")
IGNORED_DIRECTORIES = {".git", ".github", "__pycache__", "venv", ".venv"}


def calculate_project_inventory() -> str:
    """Return Markdown inventory derived from selected repository files."""
    total_files = 0
    total_lines = 0
    components: dict[str, int] = {}

    for root, dirs, files in os.walk("."):
        dirs[:] = [directory for directory in dirs if directory not in IGNORED_DIRECTORIES]

        for filename in files:
            if not filename.endswith(TARGET_EXTENSIONS):
                continue

            path = os.path.join(root, filename)
            try:
                with open(path, encoding="utf-8", errors="ignore") as handle:
                    line_count = sum(1 for _ in handle)
            except OSError:
                continue

            total_files += 1
            total_lines += line_count
            relative_parts = os.path.relpath(root, ".").split(os.sep)
            component = relative_parts[0] if relative_parts[0] != "." else "root"
            components[component] = components.get(component, 0) + line_count

    output = [
        "## Repository inventory\n",
        "\n",
        "> Generated from selected text files in this checkout. This is an inventory, not a performance, safety, accuracy, or quality metric.\n",
        "\n",
        "| Inventory item | Value |\n",
        "| :--- | ---: |\n",
        f"| Selected text files | {total_files} |\n",
        f"| Lines in selected text files | {total_lines} |\n",
    ]
    for component, line_count in sorted(components.items(), key=lambda item: item[1], reverse=True)[:5]:
        output.append(f"| `{component}` selected-file lines | {line_count} |\n")
    return "".join(output)


if __name__ == "__main__":
    print(calculate_project_inventory())
