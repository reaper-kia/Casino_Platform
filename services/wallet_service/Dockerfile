FROM python:3.13-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:0.11.29 /uv /uvx /bin/

WORKDIR /app/services/wallet_service

COPY packages/platform_contracts /app/packages/platform_contracts
COPY services/wallet_service/pyproject.toml services/wallet_service/uv.lock services/wallet_service/README.md ./

RUN uv sync --locked --no-dev --no-install-project

COPY services/wallet_service/src ./src

RUN uv sync --locked --no-dev

ENV PATH="/app/services/wallet_service/.venv/bin:$PATH"

EXPOSE 50053

CMD ["wallet-service"]