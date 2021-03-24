FROM tiangolo/uvicorn-gunicorn:python3.8-alpine3.10

ARG VERSION

RUN apk add --no-cache g++ musl-dev libffi-dev \
    && pip install --no-cache-dir kess==${VERSION} \
    && apk del g++ musl-dev libffi-dev

ADD examples /app
