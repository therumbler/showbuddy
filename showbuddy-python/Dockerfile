FROM python:3.13.1

WORKDIR /app
EXPOSE 8000
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install uv
COPY uv.lock /app/uv.lock
COPY  pyproject.toml /app/pyproject.toml
RUN uv sync
COPY . .
ENTRYPOINT [ "./entrypoint.sh" ]
