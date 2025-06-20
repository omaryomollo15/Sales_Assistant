#!/bin/bash
source /opt/venv/bin/activate
echo "Starting Rasa Action Server on port $PORT"
exec rasa-sdk --actions actions --port "$PORT" --debug
