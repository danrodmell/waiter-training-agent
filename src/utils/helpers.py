"""
Helper utilities for the Waiter Training Agent
"""

import os
import yaml
import logging
from typing import Dict, Any
from pathlib import Path


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        # Handle environment variable substitution
        config = _substitute_env_vars(config)
        
        return config
    except FileNotFoundError:
        print(f"Configuration file not found: {config_path}")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing configuration file: {e}")
        return {}


def _substitute_env_vars(config: Any) -> Any:
    """Recursively substitute environment variables in configuration"""
    if isinstance(config, dict):
        return {key: _substitute_env_vars(value) for key, value in config.items()}
    elif isinstance(config, list):
        return [_substitute_env_vars(item) for item in config]
    elif isinstance(config, str) and config.startswith("${") and config.endswith("}"):
        env_var = config[2:-1]
        return os.getenv(env_var, config)
    else:
        return config


def setup_logging(config: Dict[str, Any]) -> logging.Logger:
    """Set up logging configuration"""
    logger = logging.getLogger("waiter_training_agent")
    
    # Set log level
    log_level = config.get("level", "INFO")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if specified
    log_file = config.get("file")
    if log_file:
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def ensure_directories(config: Dict[str, Any]) -> None:
    """Ensure all necessary directories exist"""
    directories = [
        "data",
        "logs",
        "config"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)


def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration file"""
    required_sections = ["agent", "training", "ai"]
    
    for section in required_sections:
        if section not in config:
            print(f"Missing required configuration section: {section}")
            return False
    
    return True 