FROM rasa/rasa:3.6.0
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN rasa telemetry disable
EXPOSE $PORT
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "$PORT", "--model", "models/20250619-231257-devout-skill.tar.gz", "--endpoints", "endpoints.yml"]
