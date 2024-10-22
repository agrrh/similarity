FROM python:3-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

RUN apt-get update \
  && apt-get install git -y \
  && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./ ./

RUN chmod +x /app/main.py \
  && ln -s /app/main.py /usr/local/bin/similarity

RUN mkdir /code

WORKDIR /code

CMD ["similarity", "/code"]
