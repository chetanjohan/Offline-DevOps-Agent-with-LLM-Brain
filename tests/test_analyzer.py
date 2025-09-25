import os
import tempfile
from src.analyzer.analyzer import analyze_logs


def test_analyze_single_file(tmp_path):
    p = tmp_path / "sample.log"
    p.write_text("INFO start\nERROR oops\nWARNING hmm\nCRITICAL boom\n")

    result = analyze_logs(str(p))
    assert "files" in result
    assert len(result["files"]) == 1
    summary = result["files"][0]
    assert summary["lines"] == 4
    assert summary["error"] == 1
    assert summary["warning"] == 1
    assert summary["critical"] == 1


if __name__ == "__main__":
    test_analyze_single_file(tempfile.TemporaryDirectory())
