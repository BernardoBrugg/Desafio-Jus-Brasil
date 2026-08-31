import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Settings(BaseModel):
    dataset_dir: Path = Path(os.getenv("DATASET_DIR", "/home/brb/Downloads/dados_desafio_jusbrasil/dados_desafio_jusbrasil"))
    db_path: Path = Path(os.getenv("DB_PATH", "/home/brb/Downloads/dados_desafio_jusbrasil/dados_desafio_jusbrasil/desafio1_bracis.db"))
    goldenset_path: Path = Path(os.getenv("GOLDENSET_PATH", "/home/brb/Downloads/dados_desafio_jusbrasil/dados_desafio_jusbrasil/goldenset.xlsx"))
    input_dir: Path = Path(os.getenv("INPUT_DIR", "/home/brb/Downloads/dados_desafio_jusbrasil/dados_desafio_jusbrasil/txt"))
    output_dir: Path = Path(os.getenv("OUTPUT_DIR", "./output"))
    min_iou: float = float(os.getenv("MIN_IOU", "0.5"))

def get_settings() -> Settings:
    return Settings()
