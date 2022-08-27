# FROM python:3.10.6-alpine3.16
FROM ubuntu:20.04

# Working Directory
WORKDIR /app

# Copy source code to working directory
COPY . main.py /app/

# Install packages from requirements.txt
# RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN apt-get update \
    && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3.4 \
    python3-pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]