#!/bin/sh
# Runs every time the container STARTS (not at build time), because these steps need
# things that only exist at run time: migrate needs the database to be up, and
# collectstatic needs SECRET_KEY / DEBUG, which arrive as injected env vars.
set -e                                       # abort immediately if any command fails

python manage.py migrate --noinput           # apply migrations to the (now-running) database
python manage.py collectstatic --noinput     # gather static into STATIC_ROOT for WhiteNoise

# `exec` REPLACES this shell with gunicorn so stop/restart signals reach gunicorn directly.
# 0.0.0.0 (not 127.0.0.1) so the published port is reachable from outside the container.
# Bind to $PORT when the platform sets one (Render injects it); fall back to 8000 locally
# (docker run / docker compose, where PORT is unset).
exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3
