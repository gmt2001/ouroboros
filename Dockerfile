FROM python:3.10.5-alpine

ENV TZ UTC

WORKDIR /app

COPY /requirements.txt /setup.py /ouroboros /README.md /app/

RUN apk update && apk upgrade \
    && apk add --no-cache --virtual .build-deps gcc build-base linux-headers \
    ca-certificates musl-dev python3-dev libffi-dev openssl-dev cargo \
    && pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

COPY /pyouroboros /app/pyouroboros

COPY /locales /app/locales

RUN pip install --no-cache-dir .

RUN mkdir /app/pyouroboros/hooks

VOLUME /app/pyouroboros/hooks

ENTRYPOINT ["ouroboros"]
