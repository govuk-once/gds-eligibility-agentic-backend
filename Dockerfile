FROM python:3.12-slim AS api_server
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app/src
COPY ./src/adk/pyproject.toml ./
COPY ./src/adk/uv.lock ./
COPY ./prompts /prompts
RUN apt-get update && apt-get install -y git
ENV UV_PROJECT_ENVIRONMENT=/app/.venv
RUN uv venv /app/.venv && uv sync --locked
ARG ADK_DIR='./src/adk'
COPY ${ADK_DIR} ./
EXPOSE 8000
ENTRYPOINT ["uv", "run"]
CMD ["adk", "api_server", "--a2a", "--port", "8000", "--host", "0.0.0.0"]

FROM api_server AS web
CMD ["adk", "web", "--port", "8000", "--host", "0.0.0.0"]
