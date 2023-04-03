# syntax=docker/dockerfile:1
# platform=linux/amd64

FROM ubuntu:22.04

WORKDIR /app

RUN apt update && apt -y install python3 python3-pip binutils libglu1-mesa-dev libglib2.0-0

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5800

CMD [ "python3", "src/__init__.py" ]
