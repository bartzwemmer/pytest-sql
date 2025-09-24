from pathlib import Path
from yaml import safe_load

from sql_test_demo.models import Config


def read_config(path: Path = Path("config.yaml")) -> Config:
    """
    Configure from file in root of the application
    :param path: Path to the .yaml config file
    :return: Settings
    """
    if not path.exists():
        raise FileNotFoundError(f"Config file not found at {path}")
    with open(path, "r") as f:
        cfg = safe_load(f)

    # Validate and return the config
    return Config(**cfg)

if __name__ == "__main__":
    print(read_config())