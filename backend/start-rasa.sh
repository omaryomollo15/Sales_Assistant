#!/bin/bash
source /opt/venv/bin/activate
echo "Starting Rasa Server on port $PORT"
exec rasa run --enable-api --cors "*" --port "$PORT" --model models/20250619-231757-devout-mr.tar.gz --endpoints endpoints.yml --debug
