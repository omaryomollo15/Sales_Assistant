FROM rasa/rasa:3.6.0
WORKDIR /app
COPY . /app
COPY start-rasa.sh /app/start-rasa.sh
USER root
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /app/start-rasa.sh
RUN rasa telemetry disable
USER 1001
EXPOSE $PORT
CMD ["/app/start-rasa.sh"]
