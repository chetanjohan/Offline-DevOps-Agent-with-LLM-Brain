"""analyzer.py

Simple log analyzer placeholder.

This module provides a small, offline-friendly log analysis function that
works on both files and directories. It currently counts total lines and the
number of lines containing ERROR, WARNING, and CRITICAL (case-insensitive).
The function returns a summary dict so callers (and tests) can assert on the
results.
"""

from pathlib import Path
from typing import Dict, Any


def _analyze_file(path: Path) -> Dict[str, Any]:
    summary = {"path": str(path), "lines": 0, "error": 0, "warning": 0, "critical": 0}
    try:
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for raw in fh:
                summary["lines"] += 1
                line = raw.strip().lower()
                if "error" in line:
                    summary["error"] += 1
                if "warning" in line:
                    summary["warning"] += 1
                if "critical" in line:
                    summary["critical"] += 1
    except Exception as e:
        print(f"[Analyzer] Failed to read {path}: {e}")
    return summary


def analyze_logs(log_path: str) -> Dict[str, Any]:
    """Analyze logs at the given path.

    If `log_path` is a file, analyze that file. If it's a directory, analyze
    all files that look like logs (*.log, *.txt).

    Returns a dictionary with either a single 'file' summary or an aggregated
    'files' list and overall totals.
    """
    p = Path(log_path)
    result: Dict[str, Any] = {"path": str(p), "files": [], "totals": {"lines": 0, "error": 0, "warning": 0, "critical": 0}}

    if not p.exists():
        print(f"[Analyzer] Path not found: {p}")
        return result

    if p.is_file():
        summary = _analyze_file(p)
        result["files"].append(summary)
        for k in ("lines", "error", "warning", "critical"):
            result["totals"][k] = summary[k]
        print(f"[Analyzer] Analyzed file: {p} — lines={summary['lines']}, error={summary['error']}, warning={summary['warning']}, critical={summary['critical']}")
        return result

    # directory
    patterns = ["*.log", "*.txt", "*.out"]
    files = []
    for pat in patterns:
        files.extend(p.glob(pat))

    if not files:
        print(f"[Analyzer] No log-like files found in directory: {p}")
        return result

    for f in sorted(set(files)):
        summary = _analyze_file(f)
        result["files"].append(summary)
        for k in ("lines", "error", "warning", "critical"):
            result["totals"][k] += summary[k]

    totals = result["totals"]
    print(f"[Analyzer] Analyzed {len(result['files'])} files: totals lines={totals['lines']}, error={totals['error']}, warning={totals['warning']}, critical={totals['critical']}")
    return result


if __name__ == "__main__":
    analyze_logs("path/to/logfile.log")
