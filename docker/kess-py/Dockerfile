FROM tiangolo/uvicorn-gunicorn:python3.8-alpine3.10

ARG VERSION

RUN pip install --no-cache-dir kess==${VERSION}

ADD examples /app
