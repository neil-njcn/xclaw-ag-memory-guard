# xclaw-ag-memory-guard

> **Framework:** [XClaw AgentGuard v2.3.1](https://github.com/neil-njcn/xclaw-agentguard-framework)

Memory protection for OpenClaw agents. Validates memory operations for security and integrity.

## Installation

```bash
openclaw skills install https://github.com/neil-njcn/xclaw-ag-memory-guard.git
```

## Usage

```python
from xclaw_ag_memory_guard import MemoryGuard

guard = MemoryGuard(identity="<your-identity>")

# Validate read
result = guard.validate_read("memory/path.md")
if result.allowed:
    read_memory()

# Validate write
result = guard.validate_write("memory/path.md", "content", overwrite=False)
if result.allowed:
    write_memory()
```

## Core Principle

> **Memory is identity. Corrupt memory, corrupt self.**

Validate before reading, sanitize before writing.

## Access Control (Example)

> **Note:** The following is an example access control scheme. Memory architectures vary across OpenClaw deployments. Users should customize paths and rules based on their actual setup. This example is not enforced by default.

| Level | Example Path | Example Access |
|-------|--------------|----------------|
| **Public** | `memory/*.md` | Standard |
| **Sensitive** | `memory/people/*.md` | Context-aware |
| **Private** | `.private/*` | Never expose |
| **Core** | `memory/CORE/*` | System only |

## Detectors

- **KnowledgePoisoningDetector**: False information injection
- **ContextManipulationDetector**: Context manipulation attempts

## Integration Note

`openclaw.register_interceptor()` is not implemented. Use manual validation as shown above.

## License

MIT License
