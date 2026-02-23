import csv
import json
from pathlib import Path


INPUT_FILE = "oui.csv"           # Downloaded from IEEE
OUTPUT_FILE = "oui_db.json"


def normalize_vendor_name(name: str) -> str:
    return name.strip().lower()


def build_oui_database():

    input_path = Path(INPUT_FILE)
    output_path = Path(OUTPUT_FILE)

    if not input_path.exists():
        print("❌ oui.csv not found in current directory.")
        return

    oui_dict = {}

    with open(input_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row["Registry"] != "MA-L":
                continue

            assignment = row["Assignment"].strip().upper()
            org_name = normalize_vendor_name(row["Organization Name"])

            if len(assignment) == 6:
                oui_dict[assignment] = org_name

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(oui_dict, f, indent=4)

    print(f"✅ OUI database created: {len(oui_dict)} entries")
    print(f"📁 Saved to: {output_path.resolve()}")


if __name__ == "__main__":
    build_oui_database()
