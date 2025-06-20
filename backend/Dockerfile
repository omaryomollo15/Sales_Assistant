FROM rasa/rasa:3.6.0
WORKDIR /app
COPY . /app
USER root
RUN pip install --no-cache-dir -r requirements.txt
USER 1001
RUN rasa telemetry disable
EXPOSE $PORT
CMD ["bash", "-c", "rasa run --enable-api --cors \"*\" --port $PORT --model models/20250619-231757-devout-mr.tar.gz --endpoints endpoints.yml"]
