# scripts/generate_metrics_table.py
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def calculate_project_metrics():
    # Targeted extensions for a multi-agent system layout
    target_extensions = (".py", ".json", ".yaml", ".yml", ".md")
    total_files = 0
    total_lines = 0
    components = {}

    for root, dirs, files in os.walk("."):
        # Ignore dependency environments and git history folders
        if any(
            ignored in root for ignored in ["venv", ".git", "__pycache__", ".github"]
        ):
            continue

        for file in files:
            if file.endswith(target_extensions):
                filepath = os.path.join(root, file)
                total_files += 1
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        lines = len(f.readlines())
                        total_lines += lines

                    # Categorize structural components by parent folder name
                    folder = (
                        root.split(os.sep)[1] if len(root.split(os.sep)) > 1 else "Root"
                    )
                    components[folder] = components.get(folder, 0) + lines
                except Exception:
                    continue

    # Build the markdown string structure for the README workflow.
    markdown_output = [
        "## 📊 Performance Metrics\n",
        "| Operational Dimension | Repository System Metric Value |\n",
        "| :--- | :--- |\n",
        f"| **Total Tracked Code Architecture Files** | {total_files} files |\n",
        f"| **Total Production Invariant Lines** | {total_lines} LOC |\n",
    ]

    for component, loc in sorted(components.items(), key=lambda x: x[1], reverse=True)[
        :5
    ]:
        if component != "Root":
            markdown_output.append(
                f"| **Subsystem Module: `{component}` Volume** | {loc} LOC |\n"
            )

    markdown_output.append("\n### 📈 Summary Stats")

    # Print exactly to stdout so the workflow can redirect it to TEMP_METRICS.md
    print("".join(markdown_output))


if __name__ == "__main__":
    calculate_project_metrics()
