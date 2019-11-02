#!/bin/sh

venv/bin/gunicorn src:init_app --bind 0.0.0.0:8080 --worker-class aiohttp.worker.GunicornWebWorker --reload --limit-request-field_size 1024000000 --timeout 1200
