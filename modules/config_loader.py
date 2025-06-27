import yaml
from typing import Dict, Any, Optional
import os

DEFAULT_CONFIG_PATH = 'config/default_config.yaml'

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Loads a YAML configuration file.

    If a custom path is provided, it attempts to load from there.
    If the custom path fails or is not provided, it falls back to the default path.

    Args:
        config_path: Optional path to a custom YAML configuration file.

    Returns:
        A dictionary containing the configuration.

    Raises:
        FileNotFoundError: If neither the custom nor the default config file can be found.
        yaml.YAMLError: If there is an error parsing the YAML file.
    """
    path_to_load = config_path if config_path else DEFAULT_CONFIG_PATH

    if not os.path.exists(path_to_load):
        if config_path: # If a custom path was specified but not found
            raise FileNotFoundError(f"Custom config file not found at: {config_path}")
        else: # If the default path does not exist
            raise FileNotFoundError(f"Default config file not found at: {DEFAULT_CONFIG_PATH}")

    try:
        with open(path_to_load, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        return config_data
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file at {path_to_load}: {e}")
    except Exception as e:
        raise IOError(f"Error reading file at {path_to_load}: {e}") 