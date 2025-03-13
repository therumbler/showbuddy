#!/bin/sh

uv run uvicorn --factory 'web:make_web_app' --host 0.0.0.0 --port 8000  