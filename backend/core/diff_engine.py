import difflib
from pathlib import Path


class DiffEngine:

    @staticmethod
    def generate_diff(
        previous_file: Path,
        current_file: Path,
        output_txt: Path,
        output_html: Path
    ):
        if not previous_file.exists():
            return False  # No previous file, skip diff

        previous_lines = previous_file.read_text().splitlines()
        current_lines = current_file.read_text().splitlines()

        # Generate unified diff (text)
        diff = difflib.unified_diff(
            previous_lines,
            current_lines,
            fromfile="previous",
            tofile="current",
            lineterm=""
        )

        diff_text = "\n".join(diff)

        output_txt.write_text(diff_text)

        # Generate HTML diff
        html_diff = difflib.HtmlDiff().make_file(
            previous_lines,
            current_lines,
            fromdesc="Previous",
            todesc="Current"
        )

        output_html.write_text(html_diff)

        return True
