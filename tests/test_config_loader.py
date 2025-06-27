import pytest
import yaml
import os
from modules.config_loader import load_config, DEFAULT_CONFIG_PATH

@pytest.fixture
def create_test_config(tmp_path):
    """A fixture to create temporary config files for testing."""
    def _create_file(filename, content):
        file_path = tmp_path / filename
        file_path.write_text(content, encoding='utf-8')
        return str(file_path)
    return _create_file

def test_load_config_default_path_success():
    """
    Tests that the default configuration is loaded successfully.
    Assumes config/default_config.yaml exists and is valid.
    """
    assert os.path.exists(DEFAULT_CONFIG_PATH), "Default config file must exist for this test"
    config = load_config()
    assert config is not None
    assert 'problem_patterns' in config
    assert 'stream' in config['problem_patterns']

def test_load_config_custom_path_success(create_test_config):
    """
    Tests loading a valid custom configuration file.
    """
    content = """
    problem_patterns:
      stream: 'custom_stream_pattern'
    """
    custom_config_path = create_test_config("custom.yaml", content)
    config = load_config(custom_config_path)
    assert config['problem_patterns']['stream'] == 'custom_stream_pattern'

def test_load_config_file_not_found():
    """
    Tests that FileNotFoundError is raised for a non-existent file.
    """
    with pytest.raises(FileNotFoundError) as excinfo:
        load_config("non_existent_file.yaml")
    assert "Custom config file not found" in str(excinfo.value)

def test_load_config_yaml_error(create_test_config):
    """
    Tests that YAMLError is raised for a malformed YAML file.
    """
    malformed_content = "problem_patterns: [key: value" # Invalid YAML
    malformed_config_path = create_test_config("malformed.yaml", malformed_content)
    
    with pytest.raises(yaml.YAMLError) as excinfo:
        load_config(malformed_config_path)
    assert "Error parsing YAML file" in str(excinfo.value)

def test_load_config_default_path_not_found(monkeypatch):
    """
    Tests that FileNotFoundError is raised if the default file is missing.
    """
    # Temporarily make it seem like the default file doesn't exist
    monkeypatch.setattr('os.path.exists', lambda path: False)
    with pytest.raises(FileNotFoundError) as excinfo:
        load_config()
    assert "Default config file not found" in str(excinfo.value) 