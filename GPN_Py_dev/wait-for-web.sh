#!/bin/sh
echo "Waiting for FastAPI (web) to be healthy..."
until curl -fs http://web:8000/health; do
  echo "FastAPI is not ready. Sleeping for 5 seconds..."
  sleep 5
done
echo "FastAPI is healthy. Starting Locust..."
exec locust "$@"