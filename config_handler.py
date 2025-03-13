#!/usr/bin/env python3

import os
import yaml
from typing import Dict, Any, Optional

class ConfigHandler:
    DEFAULT_CONFIG = {
        "aliases": {
            "deploy-app": {
                "job_name": "DEPLOY_my_application",
                "parameters": {
                    "TASK": "deploy",
                    "GIT_SYMBOL": "origin/master"
                },
                "options": {
                    "progress": True
                }
            }
        }
    }

    def __init__(self):
        """Initialize config handler."""
        self.config_path = os.path.expanduser("~/.jenkins-cli.yaml")
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as file:
                    return yaml.safe_load(file) or {}
            return {}
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            return {}

    def save_config(self) -> None:
        """Save configuration to YAML file."""
        try:
            with open(self.config_path, 'w') as file:
                yaml.dump(self.config, file, default_flow_style=False)
        except Exception as e:
            print(f"Error saving config: {str(e)}")

    def get_job_config(self, alias_or_name: str) -> Optional[Dict[str, Any]]:
        """Get job configuration by alias or name."""
        aliases = self.config.get('aliases', {})
        if alias_or_name in aliases:
            return aliases[alias_or_name]
        return None

    def generate_default_config(self) -> None:
        """Generate default configuration file."""
        if not os.path.exists(self.config_path):
            self.config = self.DEFAULT_CONFIG
            self.save_config()
            print(f"Default configuration generated at {self.config_path}")
        else:
            print(f"Configuration file already exists at {self.config_path}")
