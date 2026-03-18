# Quick Start Guide

## 5-Minute Setup

### 1. GitHub Action (Easiest)

Add to `.github/workflows/security.yml`:
```yaml
name: Security
on: [push, pull_request]

permissions:
  security-events: write

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: JashwanthMU/TerraSecure@v1
```

Done! Scans run automatically on every push/PR.

### 2. Docker (No Installation)
```bash
docker run --rm -v $(pwd):/scan ghcr.io/jashwanthmu/terrasecure:latest /scan
```

### 3. Local (Full Control)
```bash
git clone https://github.com/JashwanthMU/TerraSecure.git
cd TerraSecure
pip install -r requirements.txt
python src/cli.py /path/to/terraform
```

## First Scan
```bash
# Scan current directory
terrasecure .

# Specific directory
terrasecure infrastructure/

# With JSON output
terrasecure . --format json --output report.json

# Fail on high severity
terrasecure . --fail-on high
```

## View Results in GitHub

1. Run scan with SARIF output
2. Upload to GitHub Security tab
3. View findings as code scanning alerts

See [GitHub Action Guide](../ACTION_README.md) for details.