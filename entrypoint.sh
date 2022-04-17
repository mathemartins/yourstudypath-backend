#!/bin/bash

APP_PORT=${PORT:-8000}
cd /app/
#/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm yourstudypath.wsgi:application --bind "0.0.0.0:${APP_PORT}"
/opt/venv/bin/daphne yourstudypath.asgi:application --bind "0.0.0.0:${APP_PORT}"
