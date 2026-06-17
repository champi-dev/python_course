# syntax: a Dockerfile is the recipe Docker follows to build the IMAGE (the blueprint).

# Start FROM the official Python 3.14 image on a slim Debian LINUX base.
# Because the container is Linux, gunicorn (which needs Unix fork) finally runs —
# even though the host laptop is Windows.
FROM python:3.14-slim

# Python-in-container hygiene:
# - PYTHONDONTWRITEBYTECODE: don't litter .pyc files into a throwaway container
# - PYTHONUNBUFFERED: stream logs straight out (unbuffered) so `docker logs` shows them live
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# The directory inside the image where the app lives and commands run.
WORKDIR /app

# Copy ONLY requirements first, then install. This ordering is deliberate: dependencies
# change rarely, so Docker caches this expensive pip-install LAYER and reuses it on every
# rebuild where requirements.txt is unchanged — only the code copy below re-runs.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the source into the image (changes often → kept after the cached layer).
COPY . .

# Document the port the app listens on (informational; actually published at `docker run -p`).
EXPOSE 8000

# Run the entrypoint script on container start: it does migrate + collectstatic (which need
# the DB and env vars — only available at RUN time, not build time) and then execs gunicorn.
# Invoked via `sh` so the file needs no executable bit (handy on Windows).
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
