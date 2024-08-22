#!/bin/sh

exec uvicorn --factory web:make_app --host 0.0.0.0 --port 5019