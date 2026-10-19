# Maya — ShopSmart AI Customer Support Agent
# Module 04: Knowledge Base — agent.py + config.py, no tools directory, no memory
# Multi-stage build for a lean production image.

# ── Stage 1: dependency builder ───────────────────────────────────────────────
# Runs on your machine's native CPU ($BUILDPLATFORM) and downloads ready-made
# ARM64 wheels, so pip never runs under ARM64 emulation.
FROM --platform=$BUILDPLATFORM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir \
      --target=/install \
      --only-binary=:all: \
      --python-version=3.11 --implementation=cp --abi=cp311 \
      --platform=manylinux2014_aarch64 \
      --platform=manylinux_2_28_aarch64 \
      --platform=manylinux_2_34_aarch64 \
      -r requirements.txt


# ── Stage 2: runtime image ────────────────────────────────────────────────────
FROM --platform=linux/arm64 python:3.11-slim AS runtime

RUN useradd --create-home --shell /bin/bash maya
WORKDIR /app

COPY --from=builder /install /usr/local/lib/python3.11/site-packages

# Copy agent source — Module 04 has agent.py and config.py only
COPY --chown=maya:maya agent.py .
COPY --chown=maya:maya config.py .

USER maya

EXPOSE 8080

CMD ["python", "agent.py"]