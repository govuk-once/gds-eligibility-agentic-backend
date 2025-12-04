FROM python:3.12-slim AS api_server
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY . ./
RUN apt-get update && apt-get install -y git
RUN uv sync --locked
EXPOSE 8000
ENTRYPOINT ["uv", "run"]
CMD ["adk", "api_server", "--port", "8000", "--host", "0.0.0.0"]

FROM api_server AS web
CMD ["adk", "web", "--port", "8000", "--host", "0.0.0.0"]
