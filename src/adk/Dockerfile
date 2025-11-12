FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY . ./
RUN uv sync --locked
EXPOSE 8000
ENTRYPOINT ["uv", "run", "adk", "web", "--port", "8000", "--host", "0.0.0.0"]

