import yaml
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class AppConfig:
    """
    Configuration model for the application.
    """
    data_path: str


class ConfigService:
    """
    Service responsible for loading application configuration.
    """

    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path

    def load(self) -> AppConfig:
        """
        Loads configuration from a YAML file.
        Returns an AppConfig instance.
        """
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config_dict: Dict[str, Any] = yaml.safe_load(f)
                
                # Accessing nested 'data' -> 'path' from config.yaml
                data_path = config_dict.get("data", {}).get("path", "data/test.csv")
                
                return AppConfig(data_path=data_path)
        except FileNotFoundError:
            # Fallback to default if config file is missing
            return AppConfig(data_path="data/test.csv")
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration: {e}")
