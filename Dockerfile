FROM python:3.7.4-alpine3.10

WORKDIR /usr/src/app
RUN apk add build-base

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apk del build-base
COPY . .

CMD ["sh",  "bootstrap.sh" ]
