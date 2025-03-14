FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

LABEL org.opencontainers.image.source=https://github.com/gsi-upm/amor-ontology
LABEL org.opencontainers.image.description="A reference implementation for the experiments API"

EXPOSE 8000

WORKDIR /app

ADD uv.lock uv.lock
ADD pyproject.toml pyproject.toml

# Sync the project into a new environment, using the frozen lockfile
RUN uv sync --frozen

# Copy the project into the image
ADD . /app


CMD ["uv", "run", "fastapi", "run", "server.py", "--port", "8000"]
