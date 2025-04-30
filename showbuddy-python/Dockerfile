FROM python:3.13.3-alpine AS builder

WORKDIR /app

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install uv

COPY uv.lock pyproject.toml ./
RUN uv sync

FROM python:3.13.3-alpine AS runtime

EXPOSE 8000
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY . .
ENTRYPOINT [ "./entrypoint.sh" ]
