FROM python:3.9.11-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /app
WORKDIR /app
EXPOSE 8000
COPY ./team_analyzer /app
COPY ./scripts /scripts

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip && \
    pip install mkl && \
    pip install numpy && \
    pip install Bottleneck && \
    apt-get update && \
    apt-get -y install libpq-dev gcc && \
    apt-get update && apt-cache search linux-headers && \
    apt-get update && apt-get install -y postgresql-client && \
    pip install psycopg2 && \
    pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
    chown -R app:app /app/data.json && \
    chmod -R 755 /app/data.json && \
    touch /app/mysite.log && \
    chown -R app:app /app/mysite.log && \
    chmod -R 755 /app/mysite.log && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER app

CMD ["run.sh"]
