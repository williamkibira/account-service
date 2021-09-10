#!/usr/bin/env bash
PYTHONPATH=$PYTHONPATH:. \
export CONSUL_ENABLED=false
export DEBUG=true
export PORT=5600
LOG_MODE=LOCAL \
gunicorn \
    --bind 0.0.0.0:${PORT} \
    --reload \
    --logger-class app.core.logging.loggers.GunicornLogger \
'app.main:run()'

