FROM python:3.11-slim as builder

LABEL maintainer="TerraSecure Team"
LABEL version="1.0.0"
LABEL description="AI-Powered Terraform Security Scanner"

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

RUN useradd -m -u 1000 terrasecure && \
    mkdir -p /app /scan && \
    chown -R terrasecure:terrasecure /app /scan

COPY --from=builder /root/.local /home/terrasecure/.local

ENV PATH=/home/terrasecure/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY --chown=terrasecure:terrasecure . .

RUN if [ ! -f models/terrasecure_production_v1.0.pkl ]; then \
        echo "Production model not found!"; \
        echo "Building production model..."; \
        python scripts/build_production_model.py; \
    fi

USER terrasecure

VOLUME ["/scan"]

ENTRYPOINT ["python", "src/cli.py"]
CMD ["--help"]

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "from ml.ml_analyzer import MLAnalyzer; MLAnalyzer()" || exit 1

LABEL org.opencontainers.image.source="https://github.com/JashwanthMU/TerraSecure"
LABEL org.opencontainers.image.documentation="https://github.com/JashwanthMU/TerraSecure/blob/main/README.md"
LABEL org.opencontainers.image.licenses="MIT"
