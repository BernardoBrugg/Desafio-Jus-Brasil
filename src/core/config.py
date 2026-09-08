import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Settings(BaseModel):
    dataset_dir: Path = Path(os.getenv("DATASET_DIR", "./dados"))
    db_path: Path = Path(os.getenv("DB_PATH", "./dados/desafio1_bracis.db"))
    goldenset_path: Path = Path(os.getenv("GOLDENSET_PATH", "./dados/goldenset.csv"))
    input_dir: Path = Path(os.getenv("INPUT_DIR", "./dados/txt"))
    output_dir: Path = Path(os.getenv("OUTPUT_DIR", "./output"))
    min_iou: float = float(os.getenv("MIN_IOU", "0.5"))

def get_settings() -> Settings:
    return Settings()
