# backend/modules/config_compare/service.py

from pathlib import Path
import difflib


# -------------------------------------------------
# NORMALIZE FOR WHITESPACE IGNORE
# -------------------------------------------------
def normalize(line: str):
    return " ".join(line.strip().split())


# -------------------------------------------------
# MAIN COMPARE FUNCTION
# -------------------------------------------------
def compare_config_files(
    file1: Path,
    file2: Path,
    ignore_whitespace: bool = True,
    context_lines: int = 3,
):

    if not file1.exists():
        raise FileNotFoundError(f"{file1} not found")

    if not file2.exists():
        raise FileNotFoundError(f"{file2} not found")

    old_lines = file1.read_text(encoding="utf-8").splitlines()
    new_lines = file2.read_text(encoding="utf-8").splitlines()

    compare_old = [normalize(l) for l in old_lines] if ignore_whitespace else old_lines
    compare_new = [normalize(l) for l in new_lines] if ignore_whitespace else new_lines

    matcher = difflib.SequenceMatcher(None, compare_old, compare_new)

    raw_results = []

    old_line_no = 1
    new_line_no = 1

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():

        if tag == "equal":
            for o, n in zip(old_lines[i1:i2], new_lines[j1:j2]):
                raw_results.append({
                    "type": "line",
                    "old_line_no": old_line_no,
                    "new_line_no": new_line_no,
                    "old_line": o,
                    "new_line": n,
                    "status": "UNCHANGED",
                    "html_class": "line-unchanged"
                })
                old_line_no += 1
                new_line_no += 1

        elif tag == "replace":
            max_len = max(i2 - i1, j2 - j1)

            for k in range(max_len):
                old_line = old_lines[i1 + k] if i1 + k < i2 else ""
                new_line = new_lines[j1 + k] if j1 + k < j2 else ""

                raw_results.append({
                    "type": "line",
                    "old_line_no": old_line_no if old_line else None,
                    "new_line_no": new_line_no if new_line else None,
                    "old_line": old_line,
                    "new_line": new_line,
                    "status": "MODIFIED",
                    "html_class": "line-modified"
                })

                if old_line:
                    old_line_no += 1
                if new_line:
                    new_line_no += 1

        elif tag == "delete":
            for line in old_lines[i1:i2]:
                raw_results.append({
                    "type": "line",
                    "old_line_no": old_line_no,
                    "new_line_no": None,
                    "old_line": line,
                    "new_line": "",
                    "status": "REMOVED",
                    "html_class": "line-removed"
                })
                old_line_no += 1

        elif tag == "insert":
            for line in new_lines[j1:j2]:
                raw_results.append({
                    "type": "line",
                    "old_line_no": None,
                    "new_line_no": new_line_no,
                    "old_line": "",
                    "new_line": line,
                    "status": "NEW",
                    "html_class": "line-new"
                })
                new_line_no += 1

    # -------------------------------------------------
    # COLLAPSE UNCHANGED BLOCKS
    # -------------------------------------------------
    final_results = []
    buffer = []

    def flush_buffer():
        nonlocal buffer
        if not buffer:
            return

        if len(buffer) > context_lines * 2:
            # keep first context_lines
            final_results.extend(buffer[:context_lines])

            final_results.append({
                "type": "collapsed",
                "count": len(buffer) - (context_lines * 2),
                "message": f"{len(buffer) - (context_lines * 2)} unchanged lines collapsed"
            })

            # keep last context_lines
            final_results.extend(buffer[-context_lines:])
        else:
            final_results.extend(buffer)

        buffer = []

    for entry in raw_results:

        if entry["status"] == "UNCHANGED":
            buffer.append(entry)
        else:
            flush_buffer()
            final_results.append(entry)

    flush_buffer()

    summary = {
        "modified": sum(1 for r in raw_results if r["status"] == "MODIFIED"),
        "new": sum(1 for r in raw_results if r["status"] == "NEW"),
        "removed": sum(1 for r in raw_results if r["status"] == "REMOVED"),
        "unchanged": sum(1 for r in raw_results if r["status"] == "UNCHANGED"),
    }

    return {
        "total_lines": len(raw_results),
        "summary": summary,
        "diff": final_results
    }
