"""
Tests for xclaw-ag-memory-guard
"""

import pytest
from xclaw_ag_memory_guard import MemoryGuard, ValidationResult, Config


def test_config_defaults():
    """Test default configuration"""
    config = Config()
    assert config.block_threshold == 0.8
    assert config.knowledge_poisoning_enabled is True


def test_guard_initialization():
    """Test guard initialization"""
    guard = MemoryGuard()
    assert guard is not None


def test_private_path_blocked():
    """Test private path access blocked"""
    guard = MemoryGuard()
    result = guard.validate_read(".private/credentials.txt", include_in_response=True)
    assert not result.allowed
    assert result.violation_type == "unauthorized_access"


def test_immutable_file_blocked():
    """Test immutable file modification blocked"""
    guard = MemoryGuard()
    result = guard.validate_write("memory/2026-03-01.md", "content", overwrite=True)
    assert not result.allowed
    assert result.violation_type == "integrity_violation"


def test_safe_operations_allowed():
    """Test safe operations are allowed"""
    guard = MemoryGuard()
    result = guard.validate_read("memory/test.md")
    assert result.allowed
    result = guard.validate_write("memory/test.md", "content", overwrite=False)
    assert result.allowed
