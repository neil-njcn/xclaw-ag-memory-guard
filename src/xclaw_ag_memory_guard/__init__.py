"""
xclaw-ag-memory-guard: Memory protection for OpenClaw agents.

This package provides memory operation validation to prevent data poisoning,
unauthorized access, and integrity violations.
"""

from .config import Config
from .detector import MemoryGuard, ValidationResult
from .interceptor import MemoryGuardInterceptor

__version__ = "1.0.0"
__author__ = "xclaw"
__email__ = "dev@xclaw.dev"

__all__ = [
    "Config",
    "MemoryGuard",
    "ValidationResult",
    "MemoryGuardInterceptor",
]


class MemoryGuardSkill:
    """
    OpenClaw skill entry point for xclaw-ag-memory-guard.
    """
    
    name = "xclaw-ag-memory-guard"
    version = __version__
    description = "Memory protection for OpenClaw agents"
    
    def __init__(self, config: dict = None):
        from .config import Config
        from .interceptor import MemoryGuardInterceptor
        
        if config:
            self.config = Config.from_dict(config)
        else:
            self.config = Config()
        
        self.interceptor = MemoryGuardInterceptor(self.config)
    
    def register(self, openclaw_app):
        openclaw_app.register_interceptor("memory_operation", self.interceptor)
    
    def get_interceptor(self):
        return self.interceptor
