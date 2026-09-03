import csv
import json
import argparse
from pathlib import Path

def encode_citations(doc: dict) -> str:
    parts = []
    for c in doc.get("citacoes", []):
        classification = c["classificacao"]
        resolution = c.get("resolucao") or {}
        canonical_id = str(resolution.get("id_canonico", "") or "").strip() or "-"
        confidence = c.get("confianca", None)
        confidence_str = "-" if confidence is None else f"{float(confidence):.4f}"
        parts.append(f"{int(c['inicio'])},{int(c['fim'])},{classification},{canonical_id},{confidence_str}")
    return "|".join(parts) if parts else "-"

def convert(input_dir: Path, output_file: Path) -> None:
    json_files = sorted(input_dir.glob("*.json"))
    rows = []
    for file_path in json_files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        doc_id = data.get("documento_id") or file_path.stem
        rows.append((doc_id, encode_citations(data)))
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["documento_id", "citacoes"])
        writer.writerows(rows)
    print(f"Generated {output_file} with {len(rows)} documents from {len(json_files)} files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=str, default="./output")
    parser.add_argument("--output-file", type=str, default="./submission.csv")
    args = parser.parse_args()
    convert(Path(args.input_dir), Path(args.output_file))
