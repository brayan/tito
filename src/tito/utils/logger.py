import logging
from datetime import datetime
from pathlib import Path
from tito.utils.path import get_output_dir

def setup_logger(name: str = "tito") -> Path:
    LOG_DIR = get_output_dir() / "logs"
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = LOG_DIR / f"{name}_{timestamp}.log"

    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    logging.info("Logger initialized.")
    return log_file
