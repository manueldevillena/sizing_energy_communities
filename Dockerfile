FROM ubuntu:latest

RUN apt update \
    && apt install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip

RUN apt install -y coinor-cbc

RUN mkdir /app
WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

CMD bash driver.sh 