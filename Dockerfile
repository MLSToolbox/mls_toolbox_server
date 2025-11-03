FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY app /app

ENV EXECUTION_MODE="prod"

ENTRYPOINT ["python3"]
CMD ["server.py"]