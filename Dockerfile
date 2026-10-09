FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.12 /uv /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Install dependencies first so code changes don't invalidate this layer
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY README.md ./
COPY src ./src
RUN uv sync --locked --no-dev

# UID 1000 matches the default user on most Linux hosts, so ./data stays writable
RUN useradd --uid 1000 --create-home app && mkdir data && chown app:app data
USER app

CMD ["/app/.venv/bin/random-game-bot"]
