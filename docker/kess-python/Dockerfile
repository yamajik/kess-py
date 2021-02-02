FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10

RUN pip install --no-cache-dir kess

ENV KESS_FUNCTIONS_FOLDER "/app/fn"

ENV KESS_LIBRARIES_FOLDER "/app/lib"

ENV KESS_PRODUCTION true

ADD examples /app
