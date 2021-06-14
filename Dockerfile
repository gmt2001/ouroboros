FROM python:3.9.5-alpine

ENV TZ UTC

WORKDIR /app

COPY /requirements.txt /setup.py /ouroboros /README.md /app/

RUN apk add --no-cache tzdata && \
    pip install --no-cache-dir -r requirements.txt

COPY /pyouroboros /app/pyouroboros

COPY /locales /app/locales

RUN pip install --no-cache-dir .

RUN mkdir /app/pyouroboros/hooks

VOLUME /app/pyouroboros/hooks

ENTRYPOINT ["ouroboros"]
