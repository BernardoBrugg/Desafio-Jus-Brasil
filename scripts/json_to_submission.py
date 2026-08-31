import csv
import json
import argparse
from pathlib import Path

def convert(input_dir: Path, output_file: Path) -> None:
    json_files = sorted(input_dir.glob("*.json"))
    rows = []

    for file_path in json_files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        doc_id = data.get("documento_id", file_path.stem)
        citations = data.get("citacoes", [])

        for idx, cit in enumerate(citations):
            resolution = cit.get("resolucao")
            id_canonico = resolution.get("id_canonico") if resolution else None
            
            rows.append({
                "documento_id": doc_id,
                "citacao_id": f"p{idx+1}",
                "inicio": cit.get("inicio"),
                "fim": cit.get("fim"),
                "trecho": cit.get("trecho", "").replace("\n", "\\n"),
                "tipo": cit.get("tipo"),
                "classificacao": cit.get("classificacao"),
                "id_canonico": id_canonico if id_canonico is not None else "",
                "confianca": cit.get("confianca", ""),
            })

    output_file.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["documento_id", "citacao_id", "inicio", "fim", "trecho", "tipo", "classificacao", "id_canonico", "confianca"]
    
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {output_file} with {len(rows)} citations from {len(json_files)} files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=str, default="./output")
    parser.add_argument("--output-file", type=str, default="./submission.csv")
    args = parser.parse_args()
    convert(Path(args.input_dir), Path(args.output_file))
