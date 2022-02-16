FROM python:3.9-slim-buster
LABEL maintainer="nailbiter"

RUN apt-get update && apt-get install -y git

COPY requirements.txt .
RUN pip3 install -r requirements.txt

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY bot.py .
COPY .envrc .env

CMD ["python3","bot.py"]
