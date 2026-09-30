#!/usr/bin/env bash
set -e

DB_PATH="${1:-./dados/desafio1_bracis.db}"
TXT_DIR="${2:-./dados/txt}"
OUTPUT_TARGET="${3:-./submission.csv}"

PYTHON_BIN="python"
if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
fi
if [ -f ".venv/bin/python" ]; then
    PYTHON_BIN=".venv/bin/python"
fi

TEMP_OUTPUT_DIR="./output"
if [[ "$OUTPUT_TARGET" == *.csv ]]; then
    OUTPUT_CSV="$OUTPUT_TARGET"
    mkdir -p "$(dirname "$OUTPUT_CSV")"
else
    TEMP_OUTPUT_DIR="$OUTPUT_TARGET"
    OUTPUT_CSV="$OUTPUT_TARGET/submission.csv"
    mkdir -p "$OUTPUT_TARGET"
fi

mkdir -p "$TEMP_OUTPUT_DIR"

PYTHONPATH=. "$PYTHON_BIN" src/cli/run_pipeline.py --input "$TXT_DIR" --output "$TEMP_OUTPUT_DIR" --db-path "$DB_PATH"

PYTHONPATH=. "$PYTHON_BIN" scripts/json_to_submission.py --input-dir "$TEMP_OUTPUT_DIR" --output-file "$OUTPUT_CSV"

PYTHONPATH=. "$PYTHON_BIN" scripts/package_submission.py --input-dir "$TEMP_OUTPUT_DIR" --zip-file "./submission.zip"
