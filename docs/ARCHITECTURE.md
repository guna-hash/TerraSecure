# TerraSecure Architecture

Complete technical architecture and design documentation.

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [ML Pipeline](#ml-pipeline)
- [AI Enhancement](#ai-enhancement)
- [CI/CD Integration](#cicd-integration)
- [Data Flow](#data-flow)
- [Components](#components)

---

## Overview

TerraSecure is a **ML-powered security scanner** for Infrastructure as Code that combines:

1. **Rule-based detection** (50+ security patterns)
2. **Machine learning** (XGBoost model, 92% accuracy)
3. **AI analysis** (AWS Bedrock + intelligent fallback)
4. **Multi-format output** (Text, JSON, SARIF 2.1.0)

---

## System Architecture

### High-Level Architecture
```mermaid
flowchart TB
    subgraph Input["📥 Input Sources"]
        TF[Terraform Files]
        HCL[HCL Configurations]
        MOD[Terraform Modules]
    end

    subgraph Parser["🔍 Parser Layer"]
        HP[HCL Parser]
        RE[Resource Extractor]
        HP --> RE
    end

    subgraph Detection["🎯 Detection Engine"]
        RULES[Rule Engine<br/>50+ Security Patterns]
        ML[ML Model<br/>XGBoost 92% Accuracy]
        FEAT[Feature Extractor<br/>50 Security Features]
        
        RULES --> |Violations|FINDINGS
        ML --> |Risk Scores|FINDINGS
        FEAT --> ML
    end

    subgraph AI["🧠 AI Analysis Layer"]
        BEDROCK[AWS Bedrock<br/>Claude 3 Haiku]
        FALLBACK[Intelligent Fallback<br/>Expert Templates]
        CACHE[Response Cache<br/>90% Cost Savings]
        
        BEDROCK --> CACHE
        CACHE --> |Cache Miss|BEDROCK
        CACHE --> |Cache Hit|ENHANCE
        FALLBACK --> ENHANCE
    end

    subgraph Output["📊 Output Formats"]
        TEXT[Text Output<br/>Human-Readable]
        JSON[JSON Output<br/>Machine-Readable]
        SARIF[SARIF 2.1.0<br/>GitHub Security]
    end

    subgraph Integration["🔗 Integration Points"]
        GH[GitHub Actions]
        DOCKER[Docker Container]
        CLI[Command Line]
        GHSEC[GitHub Security Tab]
    end

    TF --> HP
    HCL --> HP
    MOD --> HP
    
    RE --> RULES
    RE --> FEAT
    
    FINDINGS[🔍 Security Findings] --> AI
    AI --> ENHANCE[Enhanced Findings<br/>with AI Context]
    
    ENHANCE --> TEXT
    ENHANCE --> JSON
    ENHANCE --> SARIF
    
    TEXT --> CLI
    JSON --> DOCKER
    SARIF --> GH
    SARIF --> GHSEC
    
    style Input fill:#e1f5ff
    style Parser fill:#fff3e0
    style Detection fill:#ffebee
    style AI fill:#f3e5f5
    style Output fill:#e8f5e9
    style Integration fill:#fce4ec
```

---

## ML Pipeline

### Training Pipeline
```mermaid
flowchart LR
    subgraph Training["🎓 ML Training Pipeline"]
        DATA[Training Data<br/>265 Samples]
        BREACH[Real Breaches<br/>Capital One, Uber, Tesla]
        FEAT_ENG[Feature Engineering<br/>50 Features]
        XGBOOST[XGBoost Model<br/>5-Fold CV]
        EVAL[Evaluation<br/>92.45% Accuracy]
        
        DATA --> FEAT_ENG
        BREACH --> DATA
        FEAT_ENG --> XGBOOST
        XGBOOST --> EVAL
        EVAL --> |Model Export|MODEL_FILE[terrasecure_v1.0.pkl<br/>177 KB]
    end

    subgraph Inference["🔮 ML Inference"]
        RESOURCE[Terraform Resource]
        EXTRACT[Extract 50 Features]
        PREDICT[Predict Risk]
        SCORE[Risk Score<br/>0.0 - 1.0]
        CONF[Confidence Score]
        
        RESOURCE --> EXTRACT
        MODEL_FILE --> PREDICT
        EXTRACT --> PREDICT
        PREDICT --> SCORE
        PREDICT --> CONF
    end

    style Training fill:#e3f2fd
    style Inference fill:#fff8e1
```

### 50 Security Features

| Category | Features | Example |
|----------|----------|---------|
| **Network** | 12 features | `open_cidr_0_0_0_0`, `open_ssh_port_22` |
| **Storage** | 15 features | `s3_public_acl`, `s3_encryption_disabled` |
| **IAM** | 10 features | `iam_wildcard_policy`, `root_account_usage` |
| **Secrets** | 8 features | `hardcoded_credentials`, `plaintext_secrets` |
| **Monitoring** | 5 features | `cloudtrail_disabled`, `no_vpc_flow_logs` |

---

## AI Enhancement

### AI Analysis Flow
```mermaid
sequenceDiagram
    participant R as Resource
    participant D as Detection Engine
    participant M as ML Model
    participant A as AI Analyzer
    participant C as Cache
    participant O as Output

    R->>D: Scan Resource
    D->>D: Apply Rules
    D->>M: Extract Features
    M->>M: Predict Risk
    M-->>D: Risk Score (0.95)
    
    D->>A: Finding + Risk Score
    A->>C: Check Cache
    
    alt Cache Hit
        C-->>A: Cached Analysis
    else Cache Miss
        A->>A: Generate Prompt
        A->>A: Call Bedrock/Fallback
        A->>C: Store in Cache
    end
    
    A-->>O: Enhanced Finding
    O->>O: Format (Text/JSON/SARIF)
    O-->>R: Results with AI Context
```

### AI Enhancement Components

**AWS Bedrock Mode:**
- Model: Claude 3 Haiku
- Cost: ~$0.25/M input tokens
- With caching: ~$2-5/month for 1000 scans
- Response time: ~500ms per finding

**Fallback Mode:**
- Expert templates from real breaches
- Cost: $0 (completely free)
- Response time: <1ms per finding
- Quality: Expert-level analysis

---

## CI/CD Integration

### GitHub Actions Flow
```mermaid
flowchart TB
    subgraph Developer["👨‍💻 Developer Workflow"]
        CODE[Write Terraform]
        COMMIT[Git Commit]
        PR[Create PR]
    end

    subgraph CI["⚙️ CI/CD Pipeline"]
        TRIGGER[GitHub Actions Trigger]
        CLONE[Clone Repository]
        SCAN[TerraSecure Scan]
        SARIF_GEN[Generate SARIF]
    end

    subgraph Analysis["📊 Analysis & Results"]
        ML_CHECK[ML Risk Scoring]
        AI_EXPLAIN[AI Analysis]
        REPORT[Generate Report]
    end

    subgraph Enforcement["🚦 Policy Enforcement"]
        CRITICAL{Critical<br/>Issues?}
        BLOCK[❌ Block PR]
        APPROVE[✅ Allow PR]
    end

    subgraph Visibility["👀 Visibility"]
        GH_SEC[GitHub Security Tab]
        PR_COMMENT[PR Comments]
        ARTIFACTS[Scan Artifacts]
    end

    CODE --> COMMIT
    COMMIT --> PR
    PR --> TRIGGER
    TRIGGER --> CLONE
    CLONE --> SCAN
    SCAN --> ML_CHECK
    ML_CHECK --> AI_EXPLAIN
    AI_EXPLAIN --> REPORT
    REPORT --> SARIF_GEN
    SARIF_GEN --> CRITICAL
    
    CRITICAL -->|Yes| BLOCK
    CRITICAL -->|No| APPROVE
    
    SARIF_GEN --> GH_SEC
    REPORT --> PR_COMMENT
    REPORT --> ARTIFACTS
    
    style Developer fill:#e1f5ff
    style CI fill:#fff3e0
    style Analysis fill:#f3e5f5
    style Enforcement fill:#ffebee
    style Visibility fill:#e8f5e9
```

---

## Data Flow

### End-to-End Scan Flow

1. **Input** - Terraform files parsed with python-hcl2
2. **Extraction** - Resources and properties extracted
3. **Rule Detection** - 50+ security patterns applied
4. **Feature Extraction** - 50 ML features computed
5. **ML Prediction** - XGBoost model predicts risk (0.0-1.0)
6. **AI Enhancement** - Bedrock/fallback adds context
7. **Output** - Formatted as Text/JSON/SARIF
8. **Integration** - Uploaded to GitHub Security / CI/CD

### Example: S3 Bucket Scan
```
S3 Bucket (public-read ACL)
    ↓
Parser extracts properties
    ↓
Rule Engine detects: public_s3_with_sensitive_data
    ↓
Feature Extractor computes 50 features:
  - s3_public_acl: 1
  - s3_encryption_disabled: 1
  - s3_versioning_disabled: 1
  - ... (47 more)
    ↓
ML Model predicts:
  - Risk Score: 0.95 (95% risky)
  - Confidence: 0.92 (92% confident)
    ↓
AI Analyzer enhances:
  - Explanation: "Public S3 allows unauthorized access..."
  - Business Impact: "GDPR fines up to €20M..."
  - Attack Scenario: "Capital One breach (2019)..."
  - Fix: "Step 1: Set acl = 'private'..."
    ↓
Output (SARIF/JSON/Text)
    ↓
GitHub Security Tab shows finding
```

---

## Components

### Core Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Parser** | python-hcl2 | Parse Terraform files |
| **Rule Engine** | Python | Apply 50+ security patterns |
| **Feature Extractor** | NumPy, Pandas | Compute 50 ML features |
| **ML Model** | XGBoost | Predict risk scores |
| **AI Analyzer** | AWS Bedrock (Claude 3) | Generate explanations |
| **SARIF Formatter** | Python | GitHub Security integration |
| **CLI** | Click | Command-line interface |

### File Structure
```
TerraSecure/
├── src/
│   ├── cli.py                 # Command-line interface
│   ├── scanner/
│   │   ├── parser.py          # Terraform parser
│   │   └── analyzer.py        # Main orchestrator
│   ├── rules/
│   │   └── security_rules.py  # 50+ security patterns
│   ├── ml/
│   │   ├── ml_analyzer.py     # ML inference
│   │   └── feature_extractor.py # Feature engineering
│   ├── llm/
│   │   └── bedrock_analyzer.py # AI enhancement
│   └── formatters/
│       └── sarif_formatter.py  # SARIF output
├── models/
│   └── terrasecure_production_v1.0.pkl # Pre-trained model
├── scripts/
│   └── build_production_model.py # Model training
└── tests/
    ├── unit/           # Unit tests
    └── integration/    # Integration tests
```

---

## Performance Characteristics

### Scalability

| Metric | Value |
|--------|-------|
| **Resources/sec** | ~100-200 |
| **Memory Usage** | < 512 MB |
| **Model Load Time** | < 1 second |
| **Scan Time (100 resources)** | ~5-10 seconds |
| **Scan Time (1000 resources)** | ~50-100 seconds |

### Accuracy Metrics

| Metric | Value | Benchmark |
|--------|-------|-----------|
| **Accuracy** | 92.45% | > 85% target |
| **Precision** | 89.29% | High |
| **Recall** | 96.00% | Excellent |
| **F1 Score** | 92.54% | Balanced |
| **False Positive Rate** | 10.71% | < 15% target |
| **False Negative Rate** | 4.00% | < 5% target |

---

## Security & Privacy

### Data Handling

-  **Offline by default** - No external API calls required
-  **Local ML inference** - Model runs on your machine
-  **Optional cloud** - Bedrock is opt-in only
-  **No telemetry** - No usage data collected
-  **Open source** - Full code transparency

### Secrets Handling

-  Never logs secrets
-  Never stores credentials
-  Never sends code to external services (without opt-in)
-  Detects hardcoded secrets
-  Warns about plaintext exposure

---

## Future Architecture (v2.1+)

### v2.1: Enhanced AI

- Real-time Bedrock streaming
- Response caching improvements
- Multi-model support (Haiku + Sonnet)

### v2.2: Compliance Engine

- NIST 800-53 mapping engine
- CIS Benchmark checker
- PCI-DSS validator

### v2.3: Multi-Cloud

- Azure ARM template support
- GCP Deployment Manager
- Kubernetes manifest scanning

---

## References

- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [AWS Bedrock](https://aws.amazon.com/bedrock/)
- [SARIF 2.1.0 Specification](https://docs.oasis-open.org/sarif/sarif/v2.1.0/)
- [Terraform Documentation](https://www.terraform.io/docs)

---

© 2026 TerraSecure - Built for DevSecOps Engineers