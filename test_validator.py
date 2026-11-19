import subprocess
import sys
from pathlib import Path
import pytest

# Automatically finds Validator.py or validator.py in the same folder
VALIDATOR = Path(__file__).parent / "Validator.py"
if not VALIDATOR.exists():
    VALIDATOR = Path(__file__).parent / "validator.py"


def run(args):
    return subprocess.run(
        [sys.executable, str(VALIDATOR), *args],
        capture_output=True,
        text=True,
    )


# 1. Exit Code 0: Valid CSV file with no blank required cells and no duplicates
def test_clean_csv_exits_0(tmp_path):
    csv_file = tmp_path / "clean.csv"
    csv_file.write_text(
        "id,name,email\n"
        "1,Asha,asha@example.com\n"
        "2,Bob,bob@example.com\n",
        encoding="utf-8",
    )
    result = run([str(csv_file), "--required", "id,name,email"])
    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""


# 2. Exit Code 1: Parametrized tests for blank required cells and duplicate rows
@pytest.mark.parametrize(
    "csv_content, required_cols, expected_output",
    [
        # Case A: Blank required 'name' column on row 3
        (
            "id,name,email\n1,Asha,asha@example.com\n2,,bob@example.com\n",
            "id,name",
            "row 3: blank column name",
        ),
        # Case B: Whitespace-only cell treated as blank on row 2
        (
            "id,name,email\n1,   ,asha@example.com\n2,Bob,bob@example.com\n",
            "id,name",
            "row 2: blank column name",
        ),
        # Case C: Blank required 'email' column on row 4
        (
            "id,name,email\n1,Asha,asha@example.com\n2,Bob,bob@example.com\n3,Chen,\n",
            "id,name,email",
            "row 4: blank column email",
        ),
        # Case D: Exact duplicate row on row 3
        (
            "id,name,email\n1,Asha,asha@example.com\n1,Asha,asha@example.com\n",
            "id,name",
            "row 3: duplicate of row 2",
        ),
        # Case E: Non-adjacent duplicate row (row 4 duplicates row 2)
        (
            "id,name,email\n1,Asha,asha@example.com\n2,Bob,bob@example.com\n1,Asha,asha@example.com\n",
            "id,name",
            "row 4: duplicate of row 2",
        ),
    ],
)
def test_blank_and_duplicate_rows_exit_1(tmp_path, csv_content, required_cols, expected_output):
    csv_file = tmp_path / "invalid_data.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    result = run([str(csv_file), "--required", required_cols])
    assert result.returncode == 1
    assert expected_output in result.stdout


# 3. Exit Code 2: Required column is missing from the CSV header
def test_missing_required_column_exits_2(tmp_path):
    csv_file = tmp_path / "missing_col.csv"
    csv_file.write_text(
        "id,name\n"
        "1,Asha\n",
        encoding="utf-8",
    )
    result = run([str(csv_file), "--required", "id,email"])
    assert result.returncode == 2
    assert "error: missing required column: email" in result.stderr


# 4. Exit Code 2: Invalid command-line arguments (e.g., forgetting --required)
def test_cli_usage_error_exits_2(tmp_path):
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("id,name\n1,Asha\n", encoding="utf-8")
    # Passing an unrecognized flag triggers argparse's built-in exit code 2
    result = run([str(csv_file), "--unknown-flag", "id"])
    assert result.returncode == 2
    assert "unrecognized arguments" in result.stderr


# 5. Exit Code 2: Path that does not exist
def test_missing_file_exits_2(tmp_path):
    nonexistent_file = tmp_path / "does_not_exist.csv"
    result = run([str(nonexistent_file), "--required", "id,name"])
    assert result.returncode == 2
    assert "error: file not found:" in result.stderr
# 6. Exit Code 1: Row blank in two required columns
def test_row_blank_in_two_required_columns_exits_1(tmp_path):
    csv_file = tmp_path / "two_blanks.csv"
    csv_file.write_text(
        "id,name,email\n"
        "1,Asha,asha@example.com\n"
        "2,,\n",
        encoding="utf-8",
    )
    result = run([str(csv_file), "--required", "id,name,email"])
    assert result.returncode == 1
    assert "row 3: blank column name" in result.stdout
    assert "row 3: blank column email" in result.stdout
