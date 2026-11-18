import argparse
import csv
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path, help="The CSV file to validate")
    parser.add_argument("--required", type=str, help="The required columns")
    args = parser.parse_args()
    validate_csv(args.file, args.required)


def validate_csv(file, required):
    if not file.exists():
        print(f"error: file not found: {file}", file=sys.stderr)
        sys.exit(2)

    columns = [name.strip() for name in required.split(",") if name.strip()]

    problems = 0
    seen = {}

    with file.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []

        missing = [name for name in columns if name not in header]
        if missing:
            for name in missing:
                print(f"error: missing required column: {name}", file=sys.stderr)
                sys.exit(2)

        for row_number, row in enumerate(reader, start=2):
            for name in columns:
                value = row.get(name) or ""
                if value.strip() == "":
                    print(f"row {row_number}: blank column {name}")
                    problems += 1

            key = tuple(row.get(name, "") for name in header)
            if key in seen:
                print(f"row {row_number}: duplicate of row {seen[key]}")
                problems += 1
            else:
                seen[key] = row_number

    if problems > 0:
        sys.exit(1)  # exit with error code 1 if there are problems
    else:  # if there are no problems, exit with success code 0
        sys.exit(0)  # exit with success code 0 if there are no problems


if __name__ == "__main__":
    main()
