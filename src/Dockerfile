FROM python:3.10-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV USING_DOCKER=1

WORKDIR /code

COPY ./src ./src
COPY requirements.txt .

COPY $CONFIG_PATH .

RUN pip install -r requirements.txt

CMD uvicorn src.app.api:app --host 0.0.0.0 --port 80 --workers $WORKERS
