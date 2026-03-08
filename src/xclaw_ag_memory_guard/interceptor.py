"""
Memory guard interceptor for OpenClaw integration.
"""

import logging
from typing import Any, Dict, Optional

from .config import Config
from .detector import MemoryGuard, ValidationResult


class MemoryGuardInterceptor:
    """Interceptor for OpenClaw memory operations."""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.guard = MemoryGuard(self.config)
        self.logger = logging.getLogger(__name__)
    
    def intercept_read(self, path: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Intercept and validate memory read."""
        include_in_response = context.get('include_in_response', True) if context else True
        result = self.guard.validate_read(path, include_in_response)
        
        return {
            'allowed': result.allowed,
            'result': result.to_dict(),
        }
    
    def intercept_write(self, path: str, content: str, 
                        overwrite: bool = False,
                        context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Intercept and validate memory write."""
        result = self.guard.validate_write(path, content, overwrite)
        
        if not result.allowed:
            self.logger.warning(f"Write blocked: {result.reason}")
        
        return {
            'allowed': result.allowed,
            'sanitized': result.sanitized_content,
            'result': result.to_dict(),
        }
