# xclaw-ag-memory-guard

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Memory protection for OpenClaw agents. Validates memory operations for security and integrity.
>
> **Framework:** [XClaw AgentGuard v2.3.1](https://github.com/neil-njcn/xclaw-agentguard-framework)

## 🛡️ Overview

`xclaw-ag-memory-guard` protects memory operations (read/write/search) to prevent data poisoning, unauthorized access, and integrity violations.

### Key Features

- 🔒 **Access Control** - Public, sensitive, private, core memory levels
- 🚫 **Immutable Protection** - Historical memory files are readonly
- 👤 **Identity Separation** - Strict boundaries between identities
- 🧠 **Poisoning Detection** - Knowledge poisoning and context manipulation

## 📦 Installation

### Via OpenClaw CLI (Recommended)

**Install from GitHub:**
```bash
openclaw skills install https://github.com/neil-njcn/xclaw-ag-memory-guard.git
```

### From Source

```bash
git clone https://github.com/neil-njcn/xclaw-ag-memory-guard.git
cd xclaw-ag-memory-guard

# Install in editable mode with virtual environment
python -m venv venv
source venv/bin/activate
pip install -e .
```

### Via pip

```bash
# Install in user environment
pip install --user xclaw-ag-memory-guard

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install xclaw-ag-memory-guard
```

## 🚀 Quick Start

After installation, the skill is ready to use. Import and use directly:

```python
from xclaw_ag_memory_guard import MemoryGuard

# Initialize with identity
guard = MemoryGuard(identity="<your-identity>")

# Validate read
result = guard.validate_read("memory/people/<user>.md")
if result.allowed:
    print("✅ Read allowed")
else:
    print(f"⚠️ Access denied: {result.reason}")

# Validate write
result = guard.validate_write("memory/2026-03-08.md", "content", overwrite=False)
if result.allowed:
    print("✅ Write allowed")
```

> **Note on Hook Integration:** Automatic hook integration is an advanced feature. Currently, OpenClaw does not provide hook interception points, so users need to manually integrate the guard into their workflow (as shown above).

## ⚙️ Configuration

Create a configuration file at `config/xclaw-ag-memory-guard.yaml`:

```yaml
# Detection threshold (0.0 - 1.0)
block_threshold: 0.8
warn_threshold: 0.5

# Detector configuration
knowledge_poisoning_enabled: true
context_manipulation_enabled: true

# Security settings
identity_separation: true
enforce_immutable: true

# Logging configuration
logging:
  level: INFO
  file: logs/memory-guard.log
```

## 📖 Usage Examples

### Basic Protection

```python
from xclaw_ag_memory_guard import MemoryGuard

guard = MemoryGuard(identity="<your-identity>")

# Read from public memory
result = guard.validate_read("memory/general.md")
print(result.allowed)  # True

# Try to modify immutable file
result = guard.validate_write("memory/2026-01-01.md", "content", overwrite=True)
print(result.allowed)   # False
print(result.violation_type)  # "integrity_violation"
```

### Custom Configuration

```python
from xclaw_ag_memory_guard import MemoryGuard, Config

config = Config(
    identity_separation=True,
    enforce_immutable=True
)

guard = MemoryGuard(identity="<your-identity>", config=config)
```

### OpenClaw Integration

> **Note:** `openclaw.register_interceptor()` is not currently implemented in OpenClaw. The example below shows the intended API for future integration:

```python
from xclaw_ag_memory_guard.interceptor import MemoryGuardInterceptor

# This API is planned but not yet available:
# interceptor = MemoryGuardInterceptor()
# openclaw.register_interceptor("memory_operation", interceptor)

# For now, use manual integration as shown in Basic Protection
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=xclaw_ag_memory_guard --cov-report=html
```

## 🔒 Security

- **Threshold Tuning**: Adjust based on your security requirements
- **Regular Updates**: Keep detector patterns updated
- **Monitoring**: Review logs regularly
- **Defense in Depth**: Use as part of comprehensive security strategy

## 🤝 Contributing

We welcome contributions!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Issue Tracker**: https://github.com/neil-njcn/xclaw-ag-memory-guard/issues

## 💬 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/neil-njcn/xclaw-ag-memory-guard/issues)

---

<p align="center">
  Made with ❤️ by KyleChen & Neil
</p>
