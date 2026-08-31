import zipfile
import argparse
from pathlib import Path

def package(input_dir: Path, zip_path: Path) -> None:
    json_files = sorted(input_dir.glob("*.json"))
    if not json_files:
        print(f"No JSON files found in {input_dir}")
        return

    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_ref:
        for file_path in json_files:
            zip_ref.write(file_path, arcname=file_path.name)

    print(f"Packaged {len(json_files)} files into {zip_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=str, default="./output")
    parser.add_argument("--zip-file", type=str, default="./submission.zip")
    args = parser.parse_args()
    package(Path(args.input_dir), Path(args.zip_file))
