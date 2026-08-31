# CLI Module

## Responsibility
Provides executable entry points for command-line execution, batch processing, and benchmark evaluation.

## Internal Architecture
- `run_pipeline.py`: Main entry point for processing input files and generating output JSON submissions.
- `run_evaluation.py`: Evaluates predictions against the golden set and prints benchmark scorecards.

## Usage Data Flow
- **Input**: CLI arguments (`--input`, `--output`, `--db-path`, `--golden-path`).
- **Output**: Output JSON files and terminal benchmark tables.
