import yaml
from typing import Dict, Any, Optional
import os

DEFAULT_CONFIG_PATH = 'config/default_config.yaml'

def _validate_config(config: Dict[str, Any], path: str):
    """
    Validates that the loaded configuration contains the required keys.
    Raises ValueError if a required key is missing.
    """
    required_keys = {
        'problem_patterns': ['stream', 'final'],
        'explanation_patterns': ['sub_item', 'first_item_delimiter', 'item_split_delimiter']
    }

    for main_key, sub_keys in required_keys.items():
        if main_key not in config:
            raise ValueError(f"Missing required section '{main_key}' in config file: {path}")
        if not isinstance(config[main_key], dict):
            raise ValueError(f"Section '{main_key}' must be a dictionary in config file: {path}")
        
        for sub_key in sub_keys:
            if sub_key not in config[main_key]:
                raise ValueError(f"Missing required key '{sub_key}' in section '{main_key}' in config file: {path}")

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
        
        if config_data is None:
            raise ValueError(f"Config file is empty or invalid: {path_to_load}")
            
        _validate_config(config_data, path_to_load)
        return config_data
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file at {path_to_load}: {e}")
    except FileNotFoundError:
        raise # Re-raise the original FileNotFoundError
    except ValueError:
        raise # Re-raise the original ValueError from validation
    except Exception as e:
        raise IOError(f"An unexpected error occurred while reading file at {path_to_load}: {e}") 