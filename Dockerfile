FROM python:3.9.4-alpine

ENV TZ UTC

WORKDIR /app

COPY /requirements.txt /setup.py /ouroboros /README.md /app/

RUN apk add --no-cache tzdata && \
    pip install --no-cache-dir -r requirements.txt

COPY /pyouroboros /app/pyouroboros

RUN pip install --no-cache-dir .

RUN mkdir /app/pyouroboros/hooks

VOLUME /app/pyouroboros/hooks

ENTRYPOINT ["ouroboros"]
