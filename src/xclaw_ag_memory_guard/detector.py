"""
Memory detection logic using xclaw-agentguard framework.
"""

import logging
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

try:
    from xclaw_agentguard import (
        KnowledgePoisoningDetector,
        ContextManipulationDetector,
    )
    XCLAW_AGENTGUARD_AVAILABLE = True
except ImportError:
    XCLAW_AGENTGUARD_AVAILABLE = False
    class KnowledgePoisoningDetector:
        def detect(self, text: str) -> Dict[str, Any]:
            return {"detected": False, "confidence": 0.0, "patterns": []}
    class ContextManipulationDetector:
        def detect(self, text: str) -> Dict[str, Any]:
            return {"detected": False, "confidence": 0.0, "patterns": []}

from .config import Config


@dataclass
class ValidationResult:
    """Result of memory operation validation."""
    
    allowed: bool = True
    detected: bool = False
    confidence: float = 0.0
    violation_type: Optional[str] = None
    action: str = "allow"
    reason: Optional[str] = None
    sanitized_content: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'allowed': self.allowed,
            'detected': self.detected,
            'confidence': self.confidence,
            'violation_type': self.violation_type,
            'action': self.action,
            'reason': self.reason,
            'sanitized_content': self.sanitized_content,
            'details': self.details,
        }


class MemoryGuard:
    """Main class for memory operation validation."""
    
    READONLY_PATTERNS = [
        r"memory/\d{4}-\d{2}-\d{2}.*\.md",
        r"memory/\d{4}-\d{2}-\d{2}-\d{4}.*\.md",
    ]
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.logger = logging.getLogger(__name__)
        self._detectors: Dict[str, Any] = {}
        self._init_detectors()
    
    def _init_detectors(self) -> None:
        """Initialize enabled detectors."""
        if not XCLAW_AGENTGUARD_AVAILABLE:
            self.logger.warning("xclaw-agentguard not available")
            return
        
        if self.config.knowledge_poisoning_enabled:
            self._detectors['knowledge_poisoning'] = KnowledgePoisoningDetector()
        if self.config.context_manipulation_enabled:
            self._detectors['context_manipulation'] = ContextManipulationDetector()
    
    def validate_read(self, path: str, include_in_response: bool = True) -> ValidationResult:
        """Validate a read operation."""
        result = ValidationResult()
        
        # Check private path
        if self._is_private_path(path) and include_in_response:
            result.allowed = False
            result.detected = True
            result.violation_type = "unauthorized_access"
            result.action = "block"
            result.reason = f"Cannot expose private path in response: {path}"
            return result
        
        return result
    
    def validate_write(self, path: str, content: str, overwrite: bool = False) -> ValidationResult:
        """Validate a write operation."""
        result = ValidationResult()
        max_confidence = 0.0
        detected_issues = []
        
        # Check immutable files
        if overwrite and self._is_immutable(path):
            result.allowed = False
            result.detected = True
            result.violation_type = "integrity_violation"
            result.action = "block"
            result.reason = f"Historical memory files are immutable: {path}"
            return result
        
        # Run detectors on content
        for name, detector in self._detectors.items():
            try:
                detection = detector.detect(content)

                # Handle DetectionResult object (from xclaw-agentguard-framework v2.3.1+)
                # or dict (legacy compatibility)
                if hasattr(detection, 'detected'):
                    # DetectionResult object
                    is_detected = detection.detected
                    confidence = getattr(detection, 'confidence', 0.0)
                else:
                    # Legacy dict format
                    is_detected = detection.get('detected', False)
                    confidence = detection.get('confidence', 0.0)

                if is_detected:
                    max_confidence = max(max_confidence, confidence)
                    detected_issues.append({
                        'detector': name,
                        'confidence': confidence,
                    })
            except Exception as e:
                self.logger.error(f"Detector {name} failed: {e}")
        
        if detected_issues:
            result.detected = True
            result.confidence = max_confidence
            result.violation_type = detected_issues[0]['detector']
            result.details = {'issues': detected_issues}
            
            if max_confidence >= self.config.block_threshold:
                result.allowed = False
                result.action = "block"
                result.reason = f"Poisoning detected (confidence: {max_confidence:.2f})"
            else:
                result.action = "warn"
                result.reason = f"Suspicious content (confidence: {max_confidence:.2f})"
        
        return result
    
    def _is_private_path(self, path: str) -> bool:
        return ".private/" in path
    
    def _is_immutable(self, path: str) -> bool:
        for pattern in self.READONLY_PATTERNS:
            if re.search(pattern, path):
                return True
        return False
    
    def block_response(self) -> str:
        return "This memory operation violates security policies."
