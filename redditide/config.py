import os
from typing import Any

import yaml
from collections import UserDict


class Config(UserDict):
    def __init__(self, filename: str) -> None:
        config_data = self.load_config(filename)
        super().__init__(config_data)

    @staticmethod
    def load_config(filename: str) -> dict[str, Any]:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "..", filename)
        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
            return config
        except (FileNotFoundError, PermissionError) as e:
            print(f"Error loading config file: {e}")
            return {}

    def get(self, key: str, default: Any | None = None) -> Any | None:
        keys = key.split(".")
        value = self.data.copy()

        for key in keys:
            value = value.get(key, default)
            if value is default:
                return default

        return value


config = Config("config.yaml")
