"""
Configuration management for xclaw-ag-memory-guard.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


@dataclass
class Config:
    """Configuration for memory guard."""
    
    block_threshold: float = 0.8
    warn_threshold: float = 0.5
    
    knowledge_poisoning_enabled: bool = True
    context_manipulation_enabled: bool = True
    
    identity_separation: bool = True
    enforce_immutable: bool = True
    
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    def __post_init__(self):
        if not 0 <= self.block_threshold <= 1:
            raise ValueError("block_threshold must be between 0 and 1")
        if not 0 <= self.warn_threshold <= 1:
            raise ValueError("warn_threshold must be between 0 and 1")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        valid_fields = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**valid_fields)
    
    @classmethod
    def from_file(cls, path: str) -> "Config":
        if not YAML_AVAILABLE:
            logging.warning("PyYAML not available")
            return cls()
        try:
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
            return cls.from_dict(data or {})
        except Exception as e:
            logging.error(f"Failed to load config: {e}")
            return cls()
