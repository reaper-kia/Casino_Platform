FROM python:3.13-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:0.11.29 /uv /uvx /bin/

WORKDIR /app/services/casino_service

COPY packages/platform_contracts /app/packages/platform_contracts
COPY services/casino_service/pyproject.toml services/casino_service/uv.lock services/casino_service/README.md ./

RUN uv sync --locked --no-dev --no-install-project

COPY services/casino_service/src ./src

RUN uv sync --locked --no-dev

ENV PATH="/app/services/casino_service/.venv/bin:$PATH"

EXPOSE 50051

CMD ["casino-service"]