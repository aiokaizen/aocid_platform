#!/usr/bin/env bash
# Redeploy the aocid platform from committed source.
# Run on the server: bash /opt/aocid/aocid_platform/deploy/deploy.sh
set -euo pipefail
REPO_DIR="/opt/aocid/aocid_platform"
COMPOSE_DIR="/opt/aocid"

cd "$REPO_DIR"
echo "==> Pulling latest code (main)..."
git pull --ff-only origin main

echo "==> Syncing infra files to compose dir..."
cp deploy/docker-compose.yml "$COMPOSE_DIR/docker-compose.yml"
cp deploy/nginx.conf         "$COMPOSE_DIR/nginx.conf"

cd "$COMPOSE_DIR"
echo "==> Building image & recreating web/nginx (db untouched)..."
docker compose up -d --build web nginx

echo "==> Containers:"
docker compose ps
echo "==> Done. The web container runs migrate + collectstatic on start."
